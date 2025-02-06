import datetime
import os

import pytest
from pandera.errors import SchemaError

from pancham.data_frame_configuration import DataFrameConfiguration
from pancham.data_frame_loader import DataFrameLoader
from pancham.file_loader import ExcelFileLoader
from pancham.file_type import FileType
from pancham.reporter import PrintReporter
from pancham_configuration import StaticPanchamConfiguration


class TestDataFrameLoader:

    filename = os.path.dirname(os.path.realpath(__file__)) + "/../example/orders.xlsx"

    def test_load_example_data(self):
        loader = DataFrameLoader({FileType.EXCEL_XLSX: ExcelFileLoader()}, PrintReporter())
        configuration = DataFrameConfiguration(self.filename, FileType.EXCEL_XLSX, sheet='Sheet1')
        configuration.add_field('Order', 'Order Id', int)
        configuration.add_field('Date', 'Rec Date', datetime.datetime)
        configuration.add_dynamic_field('Sent', field_type=bool, func=lambda row: row['Disp.'] == 'X')

        data = loader.load(configuration)

        assert len(data) == 10
        assert data.loc[0, 'Order'] == 1
        assert data.loc[0, 'Date'] == datetime.datetime(2024, 12, 22)
        assert data.loc[0, 'Sent'] == True

        assert data.loc[9, 'Order'] == 10
        assert data.loc[9, 'Date'] == datetime.datetime(2024, 12, 31)
        assert data.loc[9, 'Sent'] == False

    def test_load_example_data_with_static_field(self):
        loader = DataFrameLoader({FileType.EXCEL_XLSX: ExcelFileLoader()}, PrintReporter())
        configuration = DataFrameConfiguration(self.filename, FileType.EXCEL_XLSX, sheet='Sheet1')
        configuration.add_field('Order', 'Order Id', int)
        configuration.add_dynamic_field('Sent', field_type=bool, func=lambda row: row['Disp.'] == 'X')
        configuration.add_dynamic_field('Static', field_type=str, func=lambda row: 'abc')

        data = loader.load(configuration)

        assert len(data) == 10
        assert data.loc[0, 'Order'] == 1
        assert data.loc[0, 'Sent'] == True
        assert data.loc[0, 'Static'] == 'abc'

        assert data.loc[9, 'Order'] == 10
        assert data.loc[9, 'Sent'] == False

    def test_load_example_data_with_schema_validation(self):
        loader = DataFrameLoader({FileType.EXCEL_XLSX: ExcelFileLoader()}, PrintReporter())
        configuration = DataFrameConfiguration(self.filename, FileType.EXCEL_XLSX, sheet='Sheet1')
        configuration.add_field('Order', 'Order Id', int)
        configuration.add_field('Date', 'Rec Date', int)

        with pytest.raises(SchemaError):
            loader.load(configuration)

    def test_load_example_data_with_schema_validation_and_validation_disabled(self):
        pancham_configuration = StaticPanchamConfiguration('', False, '', True)
        loader = DataFrameLoader({FileType.EXCEL_XLSX: ExcelFileLoader()}, PrintReporter(), pancham_configuration=pancham_configuration)
        configuration = DataFrameConfiguration(self.filename, FileType.EXCEL_XLSX, sheet='Sheet1')
        configuration.add_field('Order', 'Order Id', int)
        configuration.add_field('Date', 'Rec Date', int)

        data = loader.load(configuration)

        assert len(data) == 10
        assert data.loc[0, 'Order'] == 1
