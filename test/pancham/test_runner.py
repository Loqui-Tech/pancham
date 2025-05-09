import datetime
import os

from sqlalchemy import Table, MetaData, select, Integer, Column, DateTime, Boolean, String

from pancham.database.database_engine import get_db_engine, initialize_db_engine
from pancham.pancham_configuration import PanchamConfiguration
from pancham.runner import PanchamRunner
from pancham.reporter import PrintReporter


class Config(PanchamConfiguration):

    @property
    def database_connection(self) -> str:
        env_val = os.environ.get("PC_DB")
        print(f"Connection: {env_val}")
        if env_val is None:
            return "sqlite:///test.db"

        return env_val

    @property
    def source_dir(self) -> str:
        return os.path.dirname(os.path.realpath(__file__)) + "/.."


class TestRunner:

    config_file = os.path.dirname(os.path.realpath(__file__)) + "/../example/order_configuration.yml"

    def test_runner(self):
        initialize_db_engine(Config(), PrintReporter())
        metadata = MetaData()
        Table('order', metadata, Column('Order', Integer), Column('Date', DateTime), Column('Sent', Boolean))
        metadata.create_all(get_db_engine().engine)

        runner = PanchamRunner(Config())
        runner.load_and_run(configuration_file=self.config_file)

        with get_db_engine().engine.connect() as conn:
            table = Table('order', MetaData(), autoload_with=conn)

            query = select(table.c['Order', 'Date', 'Sent'])
            result = conn.execute(query).fetchall()

            assert result[0][0] == 1
            assert result[0][1] == datetime.datetime(2024, 12, 22)
            assert result[0][2] is True

            assert result[1][0] == 2
            assert result[1][1] == datetime.datetime(2024, 12, 23)
            assert result[1][2] is False

    def test_json_runner(self):
        json_file = os.path.dirname(os.path.realpath(__file__)) + "/../example/json_order_configuration.yml"
        initialize_db_engine(Config(), PrintReporter())
        metadata = MetaData()
        Table('order10', metadata, Column('customer_id', Integer), Column('customer_name', String))
        metadata.create_all(get_db_engine().engine)

        runner = PanchamRunner(Config())
        runner.load_and_run(configuration_file=json_file)

        with get_db_engine().engine.connect() as conn:
            table = Table('order10', MetaData(), autoload_with=conn)

            query = select(table.c['customer_id', 'customer_name'])
            result = conn.execute(query).fetchall()

            assert result[0][0] == 1
            assert result[0][1] == "A"

            assert result[1][0] == 1
            assert result[1][1] == "B"

    def test_json_runner_with_duplicates(self):
        table_name = "customer_no_duplicates"
        json_file = os.path.dirname(os.path.realpath(__file__)) + "/../example/json_order_configuration_drop_duplicates.yml"
        initialize_db_engine(Config(), PrintReporter())

        with get_db_engine().engine.connect() as conn:
            metadata = MetaData()
            table = Table(table_name, metadata, Column('customer_id', Integer), Column('customer_name', String))
            metadata.create_all(conn)

            runner = PanchamRunner(Config())
            runner.load_and_run(configuration_file=json_file)

            query = select(table.c['customer_id', 'customer_name'])
            result = conn.execute(query).fetchall()

            assert result[0][0] == 1
            assert result[0][1] == "A"

            assert result[1][0] == 2
            assert result[1][1] == "C"

    def test_json_runner_iterator(self):
        table_name = "jsoniter"
        json_file = os.path.dirname(os.path.realpath(__file__)) + "/../example/json_order_configuration_iterator.yml"
        initialize_db_engine(Config(), PrintReporter())

        with get_db_engine().engine.connect() as conn:
            metadata = MetaData()
            table = Table(table_name, metadata, Column('customer_id', Integer), Column('customer_name', String))
            metadata.create_all(conn)

            runner = PanchamRunner(Config())
            runner.load_and_run(configuration_file=json_file)

            query = select(table.c['customer_id', 'customer_name'])
            result = conn.execute(query).fetchall()

            assert result[0][0] == 1
            assert result[0][1] == "A"

            assert result[1][0] == 1
            assert result[1][1] == "B"

