import os
import pytest

from file_loader import ExcelFileLoader


class TestExcelFileLoader():

    def test_load_excel_file(self):
        filename = os.path.dirname(os.path.realpath(__file__)) + "/../example/orders.xlsx"

        loader = ExcelFileLoader()
        data = loader.read_file(filename, sheet = 'Sheet1')

        assert len(data) == 10

    def test_load_without_sheet(self):
        filename = os.path.dirname(os.path.realpath(__file__)) + "/../example/orders.xlsx"

        loader = ExcelFileLoader()
        with pytest.raises(ValueError):
            loader.read_file(filename)

    def test_load_missing_excel_file(self):
        filename = os.path.dirname(os.path.realpath(__file__)) + "/../not_there.xlsx"

        loader = ExcelFileLoader()

        with pytest.raises(FileNotFoundError):
            loader.read_file(filename, sheet = 'Sheet1')
