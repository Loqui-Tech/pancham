import yaml

from .configuration.field_parser import FieldParser
from .data_frame_configuration import DataFrameConfiguration
from .output_configuration import OutputConfiguration

class DataFrameConfigurationLoader:

    def __init__(self, field_parsers: list[FieldParser], output_configuration: list[OutputConfiguration]):
        self.field_parsers = field_parsers
        self.output_configuration = output_configuration

    def load(self, filename: str) -> DataFrameConfiguration:

        data = self.load_file(filename)
        sheet: str|None = None

        if "file_path" not in data or "file_type" not in data:
            raise ValueError(f"file_path and file_type are required fields in {filename}")

        if data["file_type"] == "xlsx" and "sheet" in data:
            sheet = data["sheet"]

        configuration = DataFrameConfiguration(data["file_path"], data["file_type"], sheet=sheet)

        for f in data['fields']:
            has_parsed = False
            for parser in self.field_parsers:
                if parser.can_parse_field(f):
                    field = parser.parse_field(f)
                    configuration.add_field(data_frame_field=field)
                    has_parsed = True
                    break

            if not has_parsed:
                raise ValueError(f"Could not parse field {f}")

        if 'output' in data:
            for c in self.output_configuration:
                if c.can_apply(data):
                    configuration.add_output(c.to_output_configuration(data))

        return configuration

    def load_file(self, filename: str) -> dict:
        """
        Loads the content of a given file and returns the data as a dictionary. The file
        is typically expected to contain structured data in a format such as JSON or YAML.

        :param filename: Name of the file to be loaded. The file should exist at the
            specified path and must be readable.
        :type filename: str

        :return: A dictionary containing the data loaded from the file.
        :rtype: dict
        """
        pass


class YamlDataFrameConfigurationLoader(DataFrameConfigurationLoader):

    def load_file(self, filename: str) -> dict:
        """
        Loads data from a YAML file and returns it as a dictionary.

        The method attempts to open the specified file in read mode and parse its
        content using the YAML-safe loader. The retrieved data is then returned to
        the caller as a dictionary.

        :param filename: The name of the YAML file to load.
        :type filename: str

        :return: A dictionary containing the parsed YAML file data.
        :rtype: dict
        """
        with open(filename, 'r') as file:
            return yaml.safe_load(file)