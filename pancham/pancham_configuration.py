import yaml
import os

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
        return self.__get_config_item("database_connection", "DATABASE_CONNECTION", "database_connection")

    def __get_config_item(self, name: str, env_var: str|None = None, config_name: str|None = None) -> str:
        """
        Retrieve the configuration item based on ordering priority from configuration data,
        environment variables, or configuration file data. This method checks and returns
        the value for the requested configuration item by following the hierarchy:
        config_data > environment variable > configuration file.

        :param name: The key to retrieve the configuration item from config_data.
        :type name: str
        :param env_var: The environment variable name, used as an alternative lookup.
                        This is optional and allows None.
        :type env_var: str | None
        :param config_name: The corresponding key in the configuration file if the value
                            is not found in config_data or environment variables. This is
                            optional and allows None.
        :type config_name: str | None
        :return: The resolved configuration value associated with the provided name.
        :rtype: str
        """
        if name in self.config_data:
            return self.config_data[name]

        if env_var is not None and env_var in os.environ:
            value = os.environ[env_var]
            self.config_data[name] = value
            return value

        config_file = self.__get_config_file_data()
        if config_name is not None and config_name in config_file:
            value = config_file[config_name]
            self.config_data[name] = value
            return value

    def __get_config_file_data(self) -> dict:
        """
        Retrieves data from a configuration file. If the `config_file` attribute is
        non-empty, it directly returns its content. Otherwise, it reads the configuration
        file from the path specified by the `config_file_path` attribute, parses it,
        and stores the results in the `config_file` attribute before returning it. If
        `config_file_path` is `None`, it returns an empty dictionary.

        :return: Parsed configuration data from the file or an empty dictionary.
        :rtype: dict
        """
        if self.config_file_path is None:
            return {}

        if len(self.config_file) > 0:
            return self.config_file

        with open(self.config_file_path, "r") as config_file:
            self.config_file = yaml.safe_load(config_file)
            return self.config_file