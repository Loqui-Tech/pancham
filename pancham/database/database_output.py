import pandas as pd

from data_frame_configuration import DataFrameConfiguration
from database.database_engine import DatabaseEngine, initialize_db_engine, get_db_engine
from output_configuration import OutputConfiguration, OutputWriter
from pancham_configuration import PanchamConfiguration
from reporter import Reporter

class DatabaseOutput(OutputConfiguration):

    def can_apply(self, configuration: dict):
        if not 'output' in configuration:
            return False

        db_config: dict | None = None

        for output in configuration['output']:
            if output['output_type'] == 'database':
                db_config = output['config']
                break

        if db_config is None:
            return False

        if 'table' not in db_config:
            raise ValueError('table is required in database output configuration')

        return True

    def to_output_configuration(self, configuration: dict):
        return self.__get_database_config(configuration)

    def __get_database_config(self, configuration: dict) -> dict|None:
        for output in configuration['output']:
            if output['output_type'] == 'database':
                return output

        return None

class DatabaseOutputWriter(OutputWriter):

    def write(self, data: pd.DataFrame, configuration: dict):
        get_db_engine().write_df(data, configuration['table'])
