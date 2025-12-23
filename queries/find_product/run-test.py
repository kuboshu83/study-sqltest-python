import dataclasses
from typing import List
from datetime import datetime
import sqltest

@dataclasses.dataclass
class ProductEntity:
    id: int
    name: str
    price: int
    created_at: datetime


class ProductRepository:
    def __init__(self, connection_string: str):
        self._repository = sqltest.Repository(connection_string)
    
    def get_all(self) -> List[ProductEntity]:
        sql = "select id, name, price, created_at from product"
        return list(map(
            lambda x: ProductEntity(x[0], x[1], x[2], x[3]),
            self._repository.execute_query(sql)
        ))


def assert_list_equals(expected_list: List[ProductEntity], actual_list: List[ProductEntity]) -> bool:
    if (len(expected_list) != len(actual_list)):
        sqltest.Assersion.fail(f"List length didn't match: expected={len(expected_list)}, actual={len(actual_list)}")
        return False
    for index, (expected, actual) in enumerate(zip(expected_list, actual_list)):
        if (expected != actual):
            sqltest.Assersion.fail(f"List element didn't match: index={index}, exepcted={expected}, actual={actual}")
            return False
    return True



if __name__ == '__main__':
    connection_string = sqltest.ConnectionStringBuilder.connection_string("sample_db")

    repository = ProductRepository(connection_string)

    expected = [
        ProductEntity(1, "お米", 1000, datetime.now()),
        ProductEntity(2, "お酒", 500, datetime.now()),
        ProductEntity(3, "衣類", 2000, datetime.now()),
    ]
    actual = repository.get_all()
    assert_list_equals(expected, actual)