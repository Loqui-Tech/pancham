from pancham.data_frame_field import DataFrameField

class TestDataFrameField():
    def test_is_not_dynamic(self):
        field = DataFrameField('a', 'b', str)

        assert field.is_dynamic() == False

    def test_is_dynamic(self):
        field = DataFrameField('a', 'b', str, func = lambda x: x)

        assert field.is_dynamic() == True
