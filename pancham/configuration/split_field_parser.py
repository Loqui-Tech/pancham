from pancham.data_frame_field import DataFrameField
from pancham.reporter import get_reporter
from .field_parser import FieldParser
import re

class SplitFieldParser(FieldParser):
    """
    Parser for fields that require splitting strings based on a specific character or pattern.

    This class extends the FieldParser and provides functionality to parse fields with
    splitting logic. It determines if a field can be parsed by verifying the presence
    of a specific key and function ID. The splitting operation can optionally remove
    specific patterns from the source value before splitting. The resulting segments
    are then stripped of whitespace and empty entries are excluded.

    :ivar FUNCTION_ID: Unique identifier for the split operation as required by the
        field configuration.
    :type FUNCTION_ID: str
    """

    FUNCTION_ID = "split"

    def can_parse_field(self, field: dict) -> bool:
        return self.has_function_key(field, self.FUNCTION_ID)

    def parse_field(self, field: dict) -> DataFrameField:
        properties = field[self.FUNCTION_KEY][self.FUNCTION_ID]
        split_char = properties["split_char"]
        remove_pattern = properties.get("remove_pattern", None)
        source_name = properties[FieldParser.SOURCE_NAME_KEY]
        field[self.FIELD_TYPE_KEY] = list[str]

        reporter = get_reporter()

        def extract(data: dict) -> list[str|int|float]:
            value = data[source_name]
            if remove_pattern is not None and type(value) is str:
                value = re.sub(remove_pattern, "", value)

            reporter.report_debug("Extracted value: " + str(value))

            if type(value) is int or type(value) is float:
                return [value]

            if type(value) is not str:
                return []

            splits = value.split(split_char)
            output = [x.strip() for x in splits if len(x.strip()) > 0]

            reporter.report_debug("Split value: " + str(output))
            return output

        return self.build_func_field(field, extract)
