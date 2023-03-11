import mysql.connector

from copy import deepcopy
from ...mdb_cog import MDBCog


class MySQLCog(MDBCog):
    """Static MySQL connector provider"""
    _name: str = 'mysql'
    __conn = None

    @property
    def connection(self) -> mysql.connector:
        """Get or create a new buffered DB connection connection"""
        # Remove generated settings
        conn_settings = deepcopy(self._settings)
        for key in super().default_settings:
            del conn_settings[key]
        del conn_settings['class']
        
        if not self.__conn:
            self.__conn = mysql.connector.connect(**conn_settings)

        # Reconnect
        if not self.__conn.is_connected():
            self.__conn.close()
            self.__conn = mysql.connector.connect(**conn_settings)

        return self.__conn

    @property
    def default_settings(self) -> dict:
        """Get all configurable settings of a cog"""
        return {
            **super().default_settings,
            'host': 'mysql-db',
            'user': None,
            'password': None,
            'db': None,
            'autocommit': False
        }

    def get_required_extensions(self) -> list[str]:
        """Get a list of extensions that are required to run this cog"""
        return []
