import dataclasses
from typing import List, Any
from datetime import datetime
import sqltest
import os

@dataclasses.dataclass
class Product:
    id: int
    name: str
    price: int

class TestFindProduct:
    _base_path = os.path.abspath(os.path.dirname(__file__))

    @classmethod
    def execute_nonquery_on_postgres_autocommit(cls, sql: str):
        sqltest.SqlExecutor("postgres").execute_nonquery_with_autocommit(sql)

    @classmethod
    def execute_query_on_sample_db(cls, sql: str) -> List[Any]:
        return sqltest.SqlExecutor("sample_db").execute_query(sql)


    @classmethod
    def execute_sqlfile_on_sample_db(cls, sqlfile: str):
        sqltest.SqlFileExecutor("sample_db").execute_sqlfile(sqlfile)

    @classmethod
    def setup_class(cls):
        cls.execute_nonquery_on_postgres_autocommit("""drop database if exists sample_db""")
        cls.execute_nonquery_on_postgres_autocommit("""create database sample_db""")
        cls.execute_sqlfile_on_sample_db(os.path.join(cls._base_path, "testdata", "setup.sql"))
        cls.execute_sqlfile_on_sample_db(os.path.join(cls._base_path, "find_product.sql"))

    @classmethod
    def teardown_class(cls):
        cls.execute_nonquery_on_postgres_autocommit("""drop database if exists sample_db""")

    def test_get_all(self):
        # arrange
        sql = "select id, name, price from find_product(2000)"
        
        # act
        result = list(map(lambda x: Product(x[0], x[1], x[2]), self.execute_query_on_sample_db(sql)))

        # assert
        expected = [Product(3, "衣類", 2000)]
        actual = result
        assert expected == actual