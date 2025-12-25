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