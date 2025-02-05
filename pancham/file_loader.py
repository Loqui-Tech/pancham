import pandas as pd

from .pancham_configuration import PanchamConfiguration
from .data_frame_configuration import DataFrameConfiguration


class FileLoader:
    """
    Handles the process of loading and reading files.

    A FileLoader should be able to read a file and return a DataFrame. Each child class will
    handle a type of file
    """

    def read_file_from_configuration(self, configuration: DataFrameConfiguration, pancham_configuration: PanchamConfiguration|None = None) -> pd.DataFrame:
        """
        Reads and processes a file based on the given configuration.

        This method uses the provided configuration to locate and process the
        file accordingly. It expects the configuration object to provide all
        the necessary details such as file path, format, and other processing
        instructions.

        :param configuration: Configuration object containing the details needed
            to locate and process the file.
        :type configuration: DataFrameConfiguration
        :return: A pandas DataFrame containing the data from the file.
        :rtype: pd.DataFrame
        """
        pass

    def read_file(self, filename: str, **kwargs) -> pd.DataFrame:
        """
        Reads data from the specified file into a pandas DataFrame. The file may
        include various formats supported by pandas, and additional keyword
        arguments can be provided to specify how the file should be read.

        :param filename: The name or path of the file to be read.
        :type filename: str
        :param kwargs: Additional parameters to customize how the file is read.
        :return: A pandas DataFrame containing the data from the file.
        :rtype: pd.DataFrame
        """
        pass


class ExcelFileLoader(FileLoader):
    """
    Represents a loader for Excel files, extending the functionality of a generic
    file loader. This class provides methods to read Excel files into Pandas
    DataFrame objects based on configurations or specific file settings.

    :ivar supported_formats: Specifies the file formats that this loader supports.
    :type supported_formats: list
    :ivar default_sheet: Name of the default sheet to use if not specified.
    :type default_sheet: str
    """

    def read_file_from_configuration(self, configuration: DataFrameConfiguration, pancham_configuration: PanchamConfiguration|None = None) -> pd.DataFrame:
        """
        Reads a file based on the provided configuration and returns its content as a pandas DataFrame.

        This method utilizes the file path and optionally the sheet name from the provided configuration
        to read the corresponding file. It is assumed that the configuration object contains all the
        necessary details about the file's location and format. The actual reading is delegated to
        another method which handles the file input.

        :param pancham_configuration:
        :param configuration: The configuration object containing the file path and optional sheet name.
        :type configuration: DataFrameConfiguration
        :return: A pandas DataFrame containing the contents of the file as specified in the configuration.
        :rtype: pd.DataFrame
        """
        file_path = configuration.file_path
        if pancham_configuration is not None and pancham_configuration.source_dir is not None:
            file_path = f"{pancham_configuration.source_dir}/{file_path}"

        return self.read_file(file_path, sheet = configuration.sheet)

    def read_file(self, filename: str, **kwargs) -> pd.DataFrame:
        """
        Reads a file and returns its data as a Pandas DataFrame. This method specifically
        targets Excel files and requires a sheet name to be specified in the additional
        keyword arguments. It raises an exception if the sheet name is not provided.

        :param filename: The path to the Excel file to be read.
        :type filename: str
        :param kwargs: Additional keyword arguments, including the 'sheet' parameter,
            which specifies the name of the sheet to read from the Excel file.
            This parameter is mandatory for proper functionality.
        :return: A Pandas DataFrame containing the data from the specified sheet.
        :rtype: pandas.DataFrame

        :raises ValueError: If the 'sheet' keyword argument is not present, indicating
            that the required sheet name was not supplied.
        """
        if "sheet" not in kwargs:
            raise ValueError("Sheet name must be provided for Excel files.")

        print(filename)
        return pd.read_excel(filename, sheet_name=kwargs["sheet"])