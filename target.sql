use sample_db
go

drop table if exists find_product
go

create function find_product
(
    @price int
)
returns @result table
(
    id int,
    name nvarchar(100),
    price int
)
as
begin
    insert into @result
    select id, name, price
    from product
    where price >= @price

    return
end
go