from configuration.field_parser import FieldParser
from data_frame_field import DataFrameField


class TextFieldParser(FieldParser):

    def can_parse_field(self, field: dict) -> bool:
        return 'name' in field and 'source_name' in field and 'field_type' in field and field['field_type'] != 'datetime'

    def parse_field(self, field: dict) -> DataFrameField:
        return DataFrameField(field['name'], field['source_name'], str, self.is_nullable(field))