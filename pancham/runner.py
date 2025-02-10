from .configuration.database_match_field_parser import DatabaseMatchFieldParser
from .configuration.datetime_field_parser import DateTimeFieldParser
from .configuration.part_text_extractor_parser import PartTextExtractorParser
from .configuration.static_field_parser import StaticFieldParser
from .configuration.to_int_field_parser import ToIntFieldParser
from .configuration.field_parser import FieldParser
from .configuration.match_field_parser import MatchFieldParser
from .configuration.text_field_parser import TextFieldParser
from .data_frame_configuration import DataFrameConfiguration
from .data_frame_loader import DataFrameLoader
from .data_frame_configuration_loader import YamlDataFrameConfigurationLoader
from .database.database_engine import initialize_db_engine
from .database.sql_file_loader import SqlFileLoader
from .database.database_output import DatabaseOutputWriter, DatabaseOutput
from .file_loader import FileLoader, ExcelFileLoader
from .output_configuration import OutputWriter, OutputConfiguration
from .pancham_configuration import PanchamConfiguration
from .reporter import Reporter, PrintReporter

DEFAULT_LOADERS = {
    'xlsx': ExcelFileLoader(),
    'sql_file': SqlFileLoader()
}
DEFAULT_REPORTER = PrintReporter()
DEFAULT_FIELD_PARSERS = [
    TextFieldParser(),
    MatchFieldParser(),
    DateTimeFieldParser(),
    ToIntFieldParser(),
    PartTextExtractorParser(),
    StaticFieldParser(),
    DatabaseMatchFieldParser()
]
DEFAULT_OUTPUTS = [
    DatabaseOutput()
]

class PanchamRunner:

    def __init__(self,
                 pancham_configuration: PanchamConfiguration,
                 file_loaders: dict[str, FileLoader] | None = None,
                 outputs: dict[str, OutputWriter]|None = None,
                 reporter: Reporter | None = None,
                 field_parsers: list[FieldParser] | None = None,
                 outputs_configuration: list[OutputConfiguration] | None = None
                ):
        self.pancham_configuration = pancham_configuration
        self.loaded_outputs: dict[str, OutputWriter] = {}

        if outputs is None:
            self.outputs = {}
        else:
            self.outputs = outputs
        if file_loaders is None:
            self.file_loaders = DEFAULT_LOADERS
        else:
            self.file_loaders = file_loaders

        if reporter is None:
            self.reporter = DEFAULT_REPORTER
        else:
            self.reporter = reporter

        if field_parsers is None:
            self.field_parsers = DEFAULT_FIELD_PARSERS
        else:
            self.field_parsers = field_parsers

        if outputs_configuration is None:
            self.outputs_configuration = DEFAULT_OUTPUTS
        else:
            self.outputs_configuration = outputs_configuration

    def load_and_run(self, configuration_file: str):
        configuration_loader = YamlDataFrameConfigurationLoader(field_parsers=self.field_parsers, output_configuration=self.outputs_configuration)
        configuration = configuration_loader.load(configuration_file)

        self.reporter.report_configuration(configuration)

        self.run(configuration)

    def run(self, configuration: DataFrameConfiguration):
        """
        Executes the data loading and writing process based on the provided configuration.

        The method initializes a DataFrameLoader with the given file loaders and
        reporter, then uses it to load data as specified in the input configuration.
        Once the data is loaded, it iterates over the output specifications defined
        in the configuration and writes the data to each output destination by obtaining
        the appropriate writer.

        :param configuration: Configuration object defining how the data will be
            loaded and written. This includes input details for loading the data
            and output specifications for writing the data.
        :type configuration: DataFrameConfiguration

        :return: None
        """
        initialize_db_engine(self.pancham_configuration, self.reporter)
        loader = DataFrameLoader(self.file_loaders, self.reporter, self.pancham_configuration)
        data = loader.load(configuration)

        for output in configuration.output:
            output_writer = self.__get_output(output)
            output_writer.write(data, output)


    def __get_output(self, output_config: dict) -> OutputWriter:
        """
        Retrieves or creates an output writer based on the specified output configuration.

        This method checks whether the requested output type is available in the predefined
        outputs or has been previously loaded. If the output type is not found, it attempts
        to initialize the output writer for the specified type (e.g., database). If the
        requested output type is not supported, an exception is raised.

        :param output_config: Configuration dictionary specifying the output type. Must
                              include the `output_type` key.
        :type output_config: dict
        :return: An instance of OutputWriter corresponding to the output type.
        :rtype: OutputWriter
        :raises ValueError: If the requested output type is not supported.
        """
        output_type = output_config['output_type']

        if output_type in self.outputs:
            return self.outputs[output_type]

        if output_type in self.loaded_outputs:
            return self.loaded_outputs[output_type]

        if output_type == 'database':
            initialize_db_engine(self.pancham_configuration, self.reporter)
            self.loaded_outputs[output_type] = DatabaseOutputWriter()
            return self.loaded_outputs[output_type]

        raise ValueError(f'Unsupported output type: {output_type}')



