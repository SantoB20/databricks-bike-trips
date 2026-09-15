import requests
import os
from io import BytesIO
from zipfile import ZipFile
import shutil

def download_file_from_zip(url: str, file_name: str, dir_path: str, local_path: str) -> bool:
    """
    Downloads a file from a ZIP archive at a given URL, extracts the specified file, and saves it locally.

    Args:
        url (str): The URL of the ZIP archive.
        file_name (str): The name of the file to extract from the ZIP.
        dir_path (str): The directory where the file will be saved.
        local_path (str): The local path to write the extracted file.

    Returns:
        bool: True if the file was successfully downloaded and extracted, False otherwise.
    """
    try:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error downloading from: {url}")
            return False
        os.makedirs(dir_path, exist_ok=True)
        with ZipFile(BytesIO(res.content)) as zip_file:
            with zip_file.open(file_name) as file, open(local_path, "wb") as output:
                shutil.copyfileobj(file, output)
                return True
    except Exception as e:
        raise e
    
def download_file(url: str, dir_path: str, local_path: str) -> bool:
    """
    Downloads a file from a given URL and saves it locally.

    Args:
        url (str): The URL of the file to download.
        dir_path (str): The directory where the file will be saved.
        local_path (str): The local path to write the downloaded file.

    Returns:
        bool: True if the file was successfully downloaded and saved, False otherwise.
    """
    try:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error downloading from: {url}")
            return False
        os.makedirs(dir_path, exist_ok=True)
        with open(local_path, "wb") as file:
            file.write(res.content)
            return True
    except Exception as e:
        raise e