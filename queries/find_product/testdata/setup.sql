drop table if exists product;
create table product (
    id integer primary key,
    name text not null,
    price decimal not null,
    created_at timestamp with time zone not null
);

insert into product
    (id, name, price, created_at)
values
    (1, 'お米', 1000, '2020-10-01 10:11:12'),
    (2, 'お酒', 500, '2021-09-10 03:10:59'),
    (3, '衣類', 2000, '2023-08-01 00:10:10');