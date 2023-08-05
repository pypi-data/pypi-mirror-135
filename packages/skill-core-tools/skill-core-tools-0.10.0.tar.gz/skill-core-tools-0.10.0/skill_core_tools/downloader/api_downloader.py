import logging
import os
import tempfile
from pathlib import Path
from typing import List

from gaia_sdk.api.GaiaCredentials import HMACCredentials
from gaia_sdk.gaia import Gaia, GaiaRef
from rx import operators as ops, pipe

from skill_core_tools.downloader.downloader import Downloader
from skill_core_tools.downloader.gaia_connection_data import GaiaConnectionData

logger = logging.getLogger("DataApiDownloader")


def build_file_uri(folder_name: str, file_name: str) -> str:
    tenant_id = os.environ.get("TENANT_ID")
    if not folder_name:
        return f"gaia://{tenant_id}/{file_name}"
    else:
        return f"gaia://{tenant_id}/{folder_name}/{file_name}"


def build_folder_uri(folder_name: str) -> str:
    tenant_id = os.environ.get("TENANT_ID")
    return f"gaia://{tenant_id}/{folder_name}"


def create_destination_directory(file_path: str) -> Path:
    file_split = file_path.split('/')
    file_split.pop()
    if len(file_split) > 0:
        parent_folder = "/".join(file_split)
        destination_folder = Path(tempfile.gettempdir()) / parent_folder
        if not os.path.exists(destination_folder):
            mode = 0o777
            os.makedirs(destination_folder, mode)
        return destination_folder
    return Path(tempfile.gettempdir())


def extract_file_name(file_path: str) -> Path:
    file_split = file_path.split('/')
    return file_split.pop()


class DataApiDownloader(Downloader):

    def __init__(self, gaia_ref: GaiaRef):
        self.gaia_ref = gaia_ref

    @staticmethod
    def create(connection: GaiaConnectionData) -> Downloader:
        gaia_ref = Gaia.connect(connection.url(), HMACCredentials(connection.username(),
                                                                  connection.password()))
        return DataApiDownloader(gaia_ref=gaia_ref)

    def download(self, folder_name: str, *file_names: str) -> List[Path]:
        """
        Deprecated!-> use download_file or download_folder
       It downloads the file/files which are hosted under the provided folder_name in AIOS dataApi. Files are downloaded
       in a tempFolder, but following the same subdirectory structure as the location of AIOS
       :param folder_name: Name of the folder where the files to download are hosted. If file_names is not defined, all files
       contained in folder_name are downloaded
       :param file_names: name of the files hosted under the folder name
       :returns: A list of paths of the files on the local machine
        """
        if file_names:
            for file_name in file_names:
                file_uri = build_file_uri(folder_name, file_name)
                logger.info(f"Trying to download file {file_uri} from data API")
                try:
                    downloaded_file_in_bytes: bytes = pipe(ops.first())(
                        self.gaia_ref.data(file_uri).as_bytes()).run()
                except Exception as exc:
                    logger.error("File could not be downloaded from data API")
                    raise exc
                destination_folder = Path(tempfile.gettempdir()) / folder_name
                if not os.path.exists(destination_folder):
                    mode = 0o777
                    os.makedirs(destination_folder, mode)
                dest_file_path = destination_folder / file_name

                with open(dest_file_path, mode='wb') as file:
                    file.write(downloaded_file_in_bytes)
                logger.info(f"file was successfully downloaded under {dest_file_path}")
                return [dest_file_path]
        else:
            return DataApiDownloader.download_folder(self, folder_name)

    def download_file(self, file_name: str) -> Path:
        """
        It downloads a file from AIOS DataApi. AIOS path, including the TENANT_ID is built by the method.
        e.g.
            to download file "ABC/DEF/xyz.txt' from tenant XXXX, the file_name must be 'ABC/DEF/xyz.txt'. This downloader
            will build the complete Uri (gaia://XXXX/ABC/DEF/xyz.txt) by retrieving the tenantId from the env variables
       :param file_name: Name of the file to download
       :returns: the Path of the file on the local machine
        """
        file_uri = build_file_uri(None, file_name)
        logger.info(f"Trying to download file {file_uri} from data API")
        try:
            downloaded_file_in_bytes: bytes = pipe(ops.first())(
                self.gaia_ref.data(file_uri).as_bytes()).run()
        except Exception as exc:
            logger.error("File could not be downloaded from data API")
            raise exc

        dest_file_path = create_destination_directory(file_name) / extract_file_name(file_name)

        with open(dest_file_path, mode='wb') as file:
            file.write(downloaded_file_in_bytes)
        logger.info(f"file was successfully downloaded under {dest_file_path}")
        return dest_file_path

    def download_folder(self, folder_name: str) -> List[Path]:
        """
         It downloads the files which are hosted under the provided folder_name in AIOS dataApi. Files are downloaded
       in a tempFolder, but following the same subdirectory structure as the location of AIOS
       :param file_names: name of the files hosted under the folder name
       :returns: A list of paths of the files on the local machine
        """
        file_list = []
        folder_uri = build_folder_uri(folder_name)
        result = pipe(ops.first())(self.gaia_ref.data(folder_uri).list()).run()

        for possible_file in result:
            if folder_name in possible_file.file_path:
                file_split = possible_file.file_path.split('/')
                file_list.append(DataApiDownloader.download(self, folder_name, file_split[len(file_split) - 1])[0])

        return file_list
