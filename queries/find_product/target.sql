\c sample_db;

create or replace function find_product
(
    p_price integer
)
returns table
(
    id int,
    name text,
    price int
)
as $$
    select id, name, price
    from product
    where price >= p_price
$$ language sql;