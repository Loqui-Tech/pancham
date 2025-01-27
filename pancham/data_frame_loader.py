import pandas as pd

from data_frame_configuration import DataFrameConfiguration
from file_loader import FileLoader
from reporter import Reporter

class DataFrameLoader:

    def __init__(self, file_loaders: dict[str, FileLoader], reporter: Reporter) -> None:
        self.file_loaders = file_loaders
        self.reporter = reporter

    def load(
            self,
            configuration: DataFrameConfiguration
    ) -> pd.DataFrame:

        self.reporter.report_start(configuration)
        source_df = self.__load_file(configuration)
        renamed_df = source_df.rename(columns=configuration.renames)

        for field in configuration.dynamic_fields:
            try:
                renamed_df[field.name] = field.func(renamed_df)
            except Exception as e:
                if field.suppress_errors:
                    self.reporter.report_error(e)
                else:
                    raise e

        output = renamed_df[configuration.output_fields].copy()

        configuration.schema.validate(output)

        self.reporter.report_end(configuration, output)

        return output

    def __load_file(self, configuration: DataFrameConfiguration) -> pd.DataFrame:
        file_type = configuration.file_type

        if file_type not in self.file_loaders:
            raise ValueError(f'Unsupported file type: {file_type}')

        loader = self.file_loaders[file_type]
        return loader.read_file_from_configuration(configuration)


