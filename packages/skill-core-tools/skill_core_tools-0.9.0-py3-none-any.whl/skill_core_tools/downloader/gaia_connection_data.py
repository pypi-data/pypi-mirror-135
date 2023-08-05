import os

from skill_core_tools.downloader.connection_data import ConnectionData


class GaiaConnectionData(ConnectionData):
    def __init__(self):
        self._url = os.environ.get("GAIA_API_URL",os.environ.get("AIOS_URL"))
        self._username = os.environ.get("GAIA_API_KEY",os.environ.get("AIOS_API_KEY"))
        self._password = os.environ.get("GAIA_API_SECRET",os.environ.get("AIOS_API_SECRET"))

    def url(self) -> str:
        return self._url

    def username(self) -> str:
        return self._username

    def password(self) -> str:
        return self._password
