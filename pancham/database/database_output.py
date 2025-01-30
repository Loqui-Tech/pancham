import pandas as pd

from .database_engine import get_db_engine
from pancham.output_configuration import OutputConfiguration, OutputWriter

class DatabaseOutput(OutputConfiguration):

    def can_apply(self, configuration: dict):
        if not 'output' in configuration:
            return False

        db_config: dict | None = None

        for output in configuration['output']:
            if output['output_type'] == 'database':
                db_config = output
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
