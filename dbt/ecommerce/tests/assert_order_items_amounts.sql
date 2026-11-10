
select
    order_item_id,
    gross_amount,
    discount_amount,
    net_amount

from {{ ref('fct_order_items') }}

where abs(
    gross_amount - discount_amount - net_amount
) > 0.01
