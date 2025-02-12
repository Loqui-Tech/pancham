import os
import pytest

from pancham.file_loader import ExcelFileLoader, YamlFileLoader


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

    def test_yaml_file_loader(self):
        filename = os.path.dirname(os.path.realpath(__file__)) + "/../example/orders.yaml"

        loader = YamlFileLoader()
        data = loader.read_file(filename, key = 'orders')

        assert len(data) == 2
        assert data.iloc[0]['name'] == 'A'
