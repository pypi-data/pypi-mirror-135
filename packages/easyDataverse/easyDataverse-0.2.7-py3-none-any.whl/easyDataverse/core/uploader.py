import os
import shutil

from typing import List, Optional

from pyDataverse.api import NativeApi
from pyDataverse.models import Dataset, Datafile
from easyDataverse.core.exceptions import MissingURLException, MissingCredentialsException


def upload_to_dataverse(
    json_data: str,
    dataverse_name: str,
    filenames: List[str] = None,
    p_id: str = None,
    DATAVERSE_URL: Optional[str] = None,
    API_TOKEN: Optional[str] = None
) -> str:
    """Uploads a given Dataset to the dataverse installation found in the environment variables.

    Args:
        json_data (str): JSON representation of the Dataverse dataset.
        dataverse_name (str): Name of the Dataverse where the data will be uploaded to.
        filenames (List[str], optional): List of files that should be uploaded. Can also include durectory names. Defaults to None.

    Raises:
        MissingURLException: URL to the dataverse installation is missing. Please include in your environment variables.
        MissingCredentialsException: API-Token to the dataverse installation is missing. Please include in your environment variables

    Returns:
        str: The resulting DOI of the dataset, if successful.
    """

    # Get environment variables
    if DATAVERSE_URL is None:
        try:
            DATAVERSE_URL = os.environ["DATAVERSE_URL"]

        except KeyError:
            raise MissingURLException

    if API_TOKEN is None:
        try:
            API_TOKEN = os.environ["DATAVERSE_API_TOKEN"]
        except KeyError:
            raise MissingCredentialsException

    # Initialize pyDataverse API and Dataset
    api = NativeApi(DATAVERSE_URL, API_TOKEN)
    ds = Dataset()
    ds.from_json(json_data)

    # Finally, validate the JSON
    if ds.validate_json():

        if p_id:
            # Update dataset if pid given
            response = api.create_dataset(
                dataverse_name, json_data, p_id
            )
        else:
            # Create new if no pid given
            response = api.create_dataset(
                dataverse_name, json_data
            )

        if response.json()["status"] != "OK":
            raise Exception(response.json()["message"])

        # Get response data
        ds_pid = response.json()["data"]["persistentId"]

        if filenames is not None:
            # Upload files if given
            for filename in filenames:
                __uploadFile(
                    filename=filename,
                    ds_pid=ds_pid,
                    api=api
                )

        return ds_pid

    else:
        raise Exception("Could not upload")


def __uploadFile(filename: str, ds_pid: str, api: NativeApi) -> None:
    """Uploads any file to a dataverse dataset.
    Args:
        filename (String): Path to the file
        ds_pid (String): Dataset permanent ID to upload.
        api (API): API object which is used to upload the file
    """

    # Check if its a dir
    if os.path.isdir(filename):
        shutil.make_archive("contents", 'zip', filename)
        filename = "contents.zip"

    df = Datafile()
    df.set({"pid": ds_pid, "filename": filename})
    api.upload_datafile(ds_pid, filename, df.json())
