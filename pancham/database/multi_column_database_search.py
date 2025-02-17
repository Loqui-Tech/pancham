from sqlalchemy import Table, select

from .database_engine import get_db_engine, META


class MultiColumnDatabaseSearch:
    """
    Search a database using multiple columns
    """

    def __init__(self, table_name: str, value_col: str, cast_value: None|str = None):
        self.table_name = table_name
        self.value_col = value_col
        self.cast_value = cast_value

    def get_mapped_id(self, search: dict[str, str|int|bool]) -> str|int|None:

        with get_db_engine().engine.connect() as conn:
            data_table = Table(self.table_name, META, autoload_with=conn)

            query = select(data_table.c[self.value_col])

            for k, v in search.items():
                query = query.where(data_table.c[k] == v)

            res = conn.execute(query).fetchall()

            if len(res) == 0:
                return None

            return res[0][0]
