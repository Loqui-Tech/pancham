import pandas as pd
from sqlalchemy import text

from pancham.database.database_engine import get_db_engine
from pancham.file_loader import FileLoader


class SqlFileLoader(FileLoader):
    """
    A loader class for reading SQL files and executing the SQL statements
    against a database engine to retrieve data.

    This class is used to load data from a SQL file, execute the SQL query
    on the specified database engine, and return the result as a pandas
    DataFrame.

    :ivar some_class_attribute: Description of the attribute, if any exists.
    :type some_class_attribute: type_of_the_attribute
    """

    def read_file(self, filename: str, **kwargs) -> pd.DataFrame:

        with open(filename, 'r') as sql_file:
            with get_db_engine().engine.connect() as connection:
                select = text(sql_file.read())

                return pd.read_sql(select, connection)

class SqlExecuteFileLoader(FileLoader):
    """
    A loader class for executing SQL statements against a database engine.

    This loader will not return any data, but will execute the SQL statements
    """

    def read_file(self, filename: str, **kwargs) -> pd.DataFrame:

        with open(filename, 'r') as sql_file:
            with get_db_engine().engine.connect() as connection:
                query = text(sql_file.read())

                connection.execute(query)
                connection.commit()

                return pd.DataFrame()
