import yaml


class PanchamConfiguration:
    """
    Represents the configuration settings for the Pancham application.

    This class provides access to various configurations needed by the Pancham
    application. It includes functionality for retrieving the database connection
    string and other configuration parameters essential for application operation.

    :ivar config_data: Contains the raw configuration data as loaded from a
        configuration file or environment settings.
    :type config_data: dict
    :ivar environment: Represents the current environment in which the application
        is running (e.g., 'development', 'production').
    :type environment: str
    """

    @property
    def database_connection(self) -> str:
        """
        Provides the database connection string for the application. This property
        retrieves the configured connection string used to interface with the
        database layer, supporting operations that deal with persistent data storage.

        :return: The connection string to establish a database connection.
        :rtype: str
        """
        return ""

class OrderedPanchamConfiguration(PanchamConfiguration):

    def __init__(self, config_file_path: str|None):
        self.config_file_path = config_file_path
        self.config_data = {}
        self.config_file = {}

    @property
    def database_connection(self) -> str:
        return super().database_connection

    def __get_config_file_data(self) -> dict:
        if self.config_file_path is None:
            return {}

        if len(self.config_file) > 0:
            return self.config_file

        with open(self.config_file_path, "r") as config_file:
            self.config_file = yaml.safe_load(config_file)