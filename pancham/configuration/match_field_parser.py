from configuration.field_parser import FieldParser
from data_frame_field import DataFrameField


class MatchFieldParser(FieldParser):

    def can_parse_field(self, field: dict) -> bool:
        return 'name' in field and self.is_function(field) and 'eq' in field['func']

    def parse_field(self, field: dict) -> DataFrameField:
        is_properties = field['func']['eq']

        if 'source_name' not in is_properties or 'match' not in is_properties:
            raise ValueError('Is func requires source_name and match')

        return DataFrameField(
            name=field['name'],
            nullable=self.is_nullable(field),
            source_name=None,
            field_type=bool,
            func=lambda x: x[is_properties['source_name'] == is_properties['match']]
        )