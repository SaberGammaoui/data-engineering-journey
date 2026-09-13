with source as (

    select *
    from {{ source('raw', 'orders') }}

)

select
    order_id,
    customer,
    quantity,
    price,
    order_date,
    total_amount

from source