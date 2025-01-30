import datetime
import os

from pancham.data_frame_configuration import DataFrameConfiguration
from pancham.data_frame_loader import DataFrameLoader
from pancham.file_loader import ExcelFileLoader
from pancham.file_type import FileType
from pancham.reporter import PrintReporter


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
