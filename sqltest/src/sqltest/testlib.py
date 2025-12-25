import psycopg
from typing import List, Any

class ConnectionStringBuilder:
    def __init__(self, database: str, user: str, password: str, host: str, port: int):
        self._database = database
        self._user = user
        self._password = password
        self._host = host
        self._port = port

    def to_string(self)-> str:
        return f"dbname={self._database} user={self._user} password={self._password} host={self._host} port={self._port}"

    @classmethod
    def connection_string_of(cls, database: str):
        """
        user = "sa"
        password = "change-me"
        host = "test-db"
        port = 5432
        の接続用文字列を生成します。
        """
        user = "sa"
        password = "change-me"
        host = "test-db"
        port = 5432
        return ConnectionStringBuilder(database, user, password, host, port).to_string()


class Database:

    def __init__(self, database: str):
        self._database = database
        self._sql_executor = SqlExecutor(database)
        self._sqlfile_executor = SqlFileExecutor(database)
    
    def create(self):
        self.drop()
        SqlExecutor("postgres").execute_nonquery_with_autocommit(f"create database {self._database}")

    def drop(self):
        SqlExecutor("postgres").execute_nonquery_with_autocommit(f"drop database if exists {self._database}")

    def run_query(self, sql: str) -> List[Any]:
        return self._sql_executor.execute_query(sql)
    
    def run_nonquery(self, sql: str):
        self._sql_executor.execute_nonquery(sql)

    def run_nonquery_from(self, sqlfile: str):
        self._sqlfile_executor.execute_sqlfile(sqlfile)


class SqlExecutor:
    def __init__(self, database_name: str):
        self._connection_string = ConnectionStringBuilder.connection_string_of(database_name)

    def execute_query(self, query: str) -> List[Any]:
        """
        レコードを検索して、その結果の配列を返します。
        """
        records = []
        with psycopg.connect(self._connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                for record in cursor.fetchall():
                    records.append(record)
        return records

    def execute_nonquery(self, query: str):
        """
        副作用を伴う操作を行う。
        """
        with psycopg.connect(self._connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

    def execute_nonquery_with_autocommit(self, query: str):
        """
        AutoCommitを有効にして、副作用を伴う操作を行う。
        """
        with psycopg.connect(self._connection_string, autocommit=True) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
        

class SqlFileExecutor:
    def __init__(self, database_name: str):
        self._connection_string = ConnectionStringBuilder.connection_string_of(database_name)

    def execute_sqlfile(self, sqlfile: str):
        """
        SQLファイルを読み込んで実行する。
        """
        with open(file=sqlfile, mode="r", encoding="utf-8") as f:
            sql = f.read().replace("\n", "")
            with psycopg.connect(self._connection_string) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
