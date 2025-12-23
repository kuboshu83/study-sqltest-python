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
    def connection_string(cls, database: str):
        """
        user = "sa"
        password = "change-me"
        host = "localhost"
        port = 5432
        の接続用文字列を生成します。
        """
        user = "sa"
        password = "change-me"
        host = "localhost"
        port = 5432
        return ConnectionStringBuilder(database, user, password, host, port).to_string()


class Repository:
    def __init__(self, connection_string: str):
        self.__connection_string = connection_string

    def execute_query(self, query: str) -> List[Any]:
        """
        レコードを検索して、その結果の配列を返します。
        """
        records = []
        with psycopg.connect(self.__connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                for record in cursor.fetchall():
                    records.append(record)
        return records

    def execute_nonquery(self, query: str):
        """
        テーブルに対して副作用を伴う操作を行う。
        """
        with psycopg.connect(self.__connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)


class Assersion:
    @classmethod
    def fail(cls, message: str):
        print(f"\u001b[31mFAIL\u001b[0m: {message}")

    @classmethod
    def ok(cls):
        print(f"\u001b[32mOK\u001b")