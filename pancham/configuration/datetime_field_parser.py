import datetime

from .field_parser import FieldParser
from pancham.data_frame_field import DataFrameField

class DateTimeFieldParser(FieldParser):

    def can_parse_field(self, field: dict) -> bool:
        return 'name' in field and 'source_name' in field and 'field_type' in field and field['field_type'] == 'datetime'

    def parse_field(self, field: dict) -> DataFrameField:
        return DataFrameField(field['name'], field['source_name'], datetime.datetime, self.is_nullable(field))