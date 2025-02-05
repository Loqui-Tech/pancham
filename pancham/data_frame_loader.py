import numpy as np
import pandas as pd

from .pancham_configuration import PanchamConfiguration
from .data_frame_configuration import DataFrameConfiguration
from .file_loader import FileLoader
from .reporter import Reporter

class DataFrameLoader:
    """
    A loader class designed to handle file operations and manipulate dataframes.

    This class provides functionality to load and transform data from various file types
    using specific configurations. It works with customizable file loaders, and includes
    error handling, data validation, and dynamic field computation for producing properly
    structured output.

    :ivar file_loaders: A dictionary mapping file types to their corresponding file
        loader instances. Used to delegate file reading based on the type.
    :type file_loaders: dict[str, FileLoader]
    :ivar reporter: Responsible for reporting the status of the loading process, including
        progress, errors, and other notifications.
    :type reporter: Reporter
    :ivar pancham_configuration: Optional configuration specific to the "Pancham"
        system. If provided, it is used for additional customization of the loading process.
    :type pancham_configuration: PanchamConfiguration | None
    """

    def __init__(self, file_loaders: dict[str, FileLoader], reporter: Reporter, pancham_configuration: PanchamConfiguration|None = None) -> None:
        self.file_loaders = file_loaders
        self.reporter = reporter
        self.pancham_configuration = pancham_configuration

    def load(
            self,
            configuration: DataFrameConfiguration
    ) -> pd.DataFrame:
        """
        Loads and processes data as per the given configuration.

        The function utilizes a given configuration to load a data file, apply necessary renaming
        of columns, process dynamic fields, handle errors, cast columns to specified types,
        and validate the resulting dataset against a predefined schema. It replaces `nan`
        and `-inf` values with 0. After performing all operations, the processed DataFrame
        is returned.

        :param configuration: A data frame configuration object that contains all the necessary settings
                              such as renames, dynamic fields, output fields, cast values,
                              and a validation schema.
        :type configuration: DataFrameConfiguration
        :return: A fully processed and validated pandas DataFrame.
        :rtype: pd.DataFrame
        """

        self.reporter.report_start(configuration)
        source_df = self.__load_file(configuration)
        renamed_df = source_df.rename(columns=configuration.renames)

        for field in configuration.dynamic_fields:
            try:
                renamed_df[field.name] = renamed_df.apply(field.func, axis=1)
            except Exception as e:
                if field.suppress_errors:
                    self.reporter.report_error(e)
                else:
                    raise e

        output = renamed_df[configuration.output_fields].copy()

        for key, value in configuration.cast_values.items():
            if value == 'int':
                output[key] = output[key].replace([np.nan, np.inf, -np.inf], 0)
            output[key] = output[key].astype(value)

        configuration.schema.validate(output)

        self.reporter.report_end(configuration, output)

        return output

    def __load_file(self, configuration: DataFrameConfiguration) -> pd.DataFrame:
        file_type = configuration.file_type

        if file_type not in self.file_loaders:
            raise ValueError(f'Unsupported file type: {file_type}')

        loader = self.file_loaders[file_type]
        return loader.read_file_from_configuration(configuration, self.pancham_configuration)


