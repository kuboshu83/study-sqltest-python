drop database if exists sample_db;
go
create database sample_db;
go

use sample_db;
go

drop table if exists product;
go
create table product (
    id int primary key,
    name nvarchar(100) not null,
    price int not null,
    created_at datetime2 not null
)

insert into product
    (id, name, price, created_at)
values
    (1, 'お米', 1000, '2020-10-01 10:11:12'),
    (2, 'お酒', 500, '2021-09-10 03:10:59'),
    (3, '衣類', 2000, '2023-08-01 00:10:10')
