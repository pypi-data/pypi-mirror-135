import os
import xmltodict

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, validate_arguments
from json import dumps

from easyDataverse.core.uploader import upload_to_dataverse
from easyDataverse.core.dataverseBase import DataverseBase
from easyDataverse.core.downloader import download_from_dataverse
from easyDataverse.core.exceptions import DatasetAlreadyExistsException


class Dataset(BaseModel):

    class Config:
        extra = "allow"

    metadatablocks: Dict[str, Any] = dict()
    p_id: Optional[str] = None

    # ! Adders

    def add_metadatablock(
        self,
        metadatablock: DataverseBase
    ) -> None:
        """Adds a metadatablock object to the dataset if it is of 'DataverseBase' type and has a metadatablock name"""

        # Check if the metadatablock is of 'DataverseBase' type
        if issubclass(metadatablock.__class__, DataverseBase) is False:
            raise TypeError(
                f"Expected class of type 'DataverseBase', got '{metadatablock.__class__.__name__}'"
            )

        if hasattr(metadatablock, '_metadatablock_name') is False:
            raise TypeError(
                f"The provided class {metadatablock.__class__.__name__} has no metadatablock name and is thus not compatible with this function."
            )

        # Add the metadatablock to the dataset as a dict
        block_name = getattr(metadatablock, "_metadatablock_name")
        self.metadatablocks.update(
            {block_name: metadatablock}
        )

        # ... and to the __dict__
        setattr(self, block_name, metadatablock)

    # ! Exporters

    def xml(self) -> str:
        """Returns an XML representation of the dataverse object."""

        # Turn all keys to be camelcase
        fields = self._keys_to_camel(
            {"dataset_version": self.dict()}
        )

        return xmltodict.unparse(
            fields,
            pretty=True, indent="    "
        )

    def dataverse_dict(self) -> dict:
        """Returns a dictionary representation of the dataverse dataset."""

        # Convert all blocks to the appropriate format
        blocks = {}
        for block in self.metadatablocks.values():
            blocks.update(block.dataverse_dict())

        return {
            "datasetVersion": {
                "metadataBlocks": blocks
            }
        }

    def dataverse_json(self, indent: int = 2) -> str:
        """Returns a JSON representation of the dataverse dataset."""

        return dumps(self.dataverse_dict(), indent=indent)

    # ! Dataverse interfaces

    def upload(self, dataverse_name: str, filenames: List[str] = None, base_url: Optional[str] = None, api_token: Optional[str] = None) -> str:
        """Uploads a given dataset to a Dataverse installation specified in the environment variable.

        Args:
            dataverse_name (str): Name of the target dataverse.
            filenames (List[str], optional): File or directory names which will be uploaded. Defaults to None.

        """

        self.p_id = upload_to_dataverse(
            json_data=self.dataverse_json(),
            dataverse_name=dataverse_name,
            filenames=filenames,
            p_id=self.p_id,
            DATAVERSE_URL=base_url,
            API_TOKEN=api_token
        )

        return self.p_id

    # ! Initializers

    @classmethod
    @validate_arguments
    def from_dataverse_doi(cls, doi: str):
        """Initializes a Dataset from a given Dataverse dataset.

        Args:
            doi (str): DOI of the dataverse Dataset.
            lib_name (str): Name of the library to fetch the given metadatablocks.

        Returns:
            Dataset: Resulting dataset that has been downloaded from Dataverse.
        """

        lib_name = os.environ["EASYDATAVERSE_LIB_NAME"]

        return download_from_dataverse(cls(), doi, lib_name)

    # ! Utilities

    @staticmethod
    def _snake_to_camel(word: str) -> str:
        return ''.join(x.capitalize() or '_' for x in word.split('_'))

    def _keys_to_camel(self, dictionary: dict):
        nu_dict = {}
        for key in dictionary.keys():
            if isinstance(dictionary[key], dict):
                nu_dict[
                    self._snake_to_camel(key)
                ] = self._keys_to_camel(dictionary[key])
            else:
                nu_dict[
                    self._snake_to_camel(key)
                ] = dictionary[key]
        return nu_dict
