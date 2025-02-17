from sqlalchemy import MetaData, Table, Column, String
import pandas as pd

from pancham.database.multi_column_database_search import MultiColumnDatabaseSearch
from pancham.database.database_engine import get_db_engine, initialize_db_engine
from pancham.reporter import PrintReporter
from pancham_configuration import PanchamConfiguration

class MockConfig(PanchamConfiguration):

    @property
    def database_connection(self) -> str:
        return "sqlite:///:memory:"

class TestMultiColumnDatabaseSearch:

    def test_search_nothing_found(self):
        initialize_db_engine(MockConfig(), PrintReporter())

        meta = MetaData()
        Table('mc_search', meta, Column("email", String), Column("order_id", String), Column("dept", String))
        meta.create_all(get_db_engine().engine)

        data  = pd.DataFrame({
            'email': ['a@example.com', 'b@example.com', 'a@example.com'],
            'order_id': ['1', '2', '3'],
            'dept': ['A', 'B', 'B']
        })

        get_db_engine().write_df(data, 'mc_search')

        search = MultiColumnDatabaseSearch('mc_search', 'order_id')

        value = search.get_mapped_id({'email': 'c@example.com'})
        assert value is None

        first_value = search.get_mapped_id({'email': 'a@example.com'})
        assert first_value == '1'

        second_value = search.get_mapped_id({'email': 'a@example.com', 'dept': 'B'})
        assert second_value == '3'
