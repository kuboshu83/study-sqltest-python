# 概要

PostgresSQLに接続してクエリを実行するための基本的なコードを集めたものです。
接続時のパラメータはテスト用DBに接続するためので、以下の値で固定されています。

- パスワード: change-me
- ユーザ: sa
- ホスト: localhost
- ポート: 5432

また、デフォルトで"postgres"というデータベースが用意されています。

# 使い方

## データベース操作

データベースを作成・削除する方法を紹介します。

### 接続用文字列を生成する

"postgres"に接続するための文字列を生成するには、以下のように記述します。

```python
connection = sqltest.ConnectionStringBuilder.connection_string_of("postgres")
```

### 新規のデータベースを作成する

"sample_db"というデータベースを新規に作成するには、以下のように記述します。
また、同名のデータベースが存在する場合は、一度削除してから作成します。

```python
sample_db = sqltest.Database("sample_db")
sample_db.create()
```

### データベースを削除する

"sample_db"というデータベースを削除するには、以下のように記述します。
指定されたデータベースが存在しない場合は何も起こりません。

```python
sample_db = sqltest.Database("sample_db")
sample_db.drop()
```

## SQLの実行

### 戻り値のあるクエリを実行する

"sample_db"(データベース)に対して、戻り値のあるクエリ(select)を実行するには以下のように記述します。

```python
sample_db = sqltest.Database("sample_db")
result = sample_db.run_query("select * from sample_tb")
```

### 戻り値のないクエリを実行する

"sample_db"(データベース)に対して、戻り値のないクエリ(insert)を実行するには以下のように記述します。

```python
sample_db = sqltest.Database("sample_db")
sample_db.run_nonquery("insert into sample_tb (id, name) values (1, 'akira')")
```

## SQLファイルの実行

.sqlファイルに記述されたクエリを実行します。

```python
sample_db = sqltest.Database("sample_db")
sample_db.run_nonquery_from("sample.sql")
```

ファイル内には、以下のように複数のクエリを記述することができますが、値を返すクエリは使用できません。

```sql
-- sample.sql

create table user (
    id integer primary key,
    name text not null
);

create table score (
    id integer primary key,
    score integer not null
);
```

# テスト例

sqltestを使用したテストのサンプルコードを紹介します。
サンプルはpytestを使用したものとなります。

```python
import sqltest

SETUP_QUERY = """
create table student (
    id integer primary key,
    name text not null
);

create table subject (
    id integer primary key,
    name text not null
);

create table test (
    id integer primary key,
    name text not null
);

create table score (
    student_id integer not null,
    subject_id integer not null,
    test_id integer not null,
    score integer not null,
    primary key (student_id, subject_id, test_id)
);

insert into student
    (id, name)
values
    (1, 'tanaka'),
    (2, 'sato');

insert into subject
    (id, name)
values
    (1, '数学'),
    (2, '物理');

insert into test
    (id, name)
values
    (1, '中間考査'),
    (2, '期末考査');

insert into score
    (student_id, subject_id, test_id, score)
values
    (1, 1, 1, 89),
    (1, 2, 1, 97),
    (2, 1, 1, 100),
    (2, 2, 1, 79);
"""

class TestQuery:
    sample_db = sqltest.Database("sample_db")

    @classmethod
    def setup_class(cls):
        cls.sample_db.create()
        cls.sample_db.run_nonquery(SETUP_SQL)

    @classmethod
    def teardown_class(cls):
        cls.sample_db.drop()

    def test_average(self):
        # arrange
        target_sql = """
        select
            avg(score) as average
        from
            (select score from score where student_id=1)
        """

        # act
        result = self.sample_db.run_query(target_sql)

        # assert
        expected = 93
        actual = result[0]
        assert expected == actual
```