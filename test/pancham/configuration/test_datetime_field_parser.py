from configuration.datetime_field_parser import DateTimeFieldParser

def pytest_generate_tests(metafunc):
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )

class TestDatetimeFieldParser:

    params = {
        "test_can_parse_datetime_field": [
            dict(field=dict(name= 'a', source_name = 'b', field_type = 'datetime'), expected=True),
            dict(field=dict(name='a', source_name='b', field_type='str'), expected=False),
            dict(field=dict(source_name='b', field_type='datetime'), expected=False),
        ],
        "test_parse": [
            dict(name = 'a', source_name = 'b', nullable = True),
            dict(name='a', source_name='b', nullable=False),
        ]
    }

    def test_can_parse_datetime_field(self, field, expected):
        parser = DateTimeFieldParser()

        assert parser.can_parse_field(field) == expected

    def test_parse(self, name, source_name, nullable):
        field = {
            'name': name,
            'source_name': source_name,
            'nullable': nullable
        }

        parser = DateTimeFieldParser()
        data_field = parser.parse_field(field)

        assert data_field.name == name
        assert data_field.source_name == source_name
        assert data_field.nullable == nullable
