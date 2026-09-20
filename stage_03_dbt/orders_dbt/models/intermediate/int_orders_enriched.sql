select
    order_id,
    customer,
    quantity,
    price,
    order_date,
    total_amount,

    quantity * price as recalculated_total,

    case
        when total_amount >= 200 then 'high'
        when total_amount >= 100 then 'medium'
        else 'low'
    end as order_value_segment

from {{ ref('stg_orders') }}