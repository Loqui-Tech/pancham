import datetime
import os

from pancham.data_frame_configuration_loader import YamlDataFrameConfigurationLoader
from pancham.runner import DEFAULT_FIELD_PARSERS, DEFAULT_OUTPUTS

class TestDataFrameConfigurationLoader:

    filename = os.path.dirname(os.path.realpath(__file__)) + "/../example/order_configuration.yml"

    def test_load_order_configuration(self):
        loader = YamlDataFrameConfigurationLoader(field_parsers=DEFAULT_FIELD_PARSERS, output_configuration=DEFAULT_OUTPUTS)

        config = loader.load(self.filename)

        assert len(config.fields) == 3
        assert config.fields[0].name == 'Order'
        assert config.fields[0].source_name == 'Order Id'
        assert config.fields[0].nullable is False
        assert config.fields[0].field_type == int

        assert config.fields[1].name == 'Date'
        assert config.fields[1].nullable is False
        assert config.fields[1].field_type == datetime.datetime

