select
    order_item_id,
    gross_amount,
    discount_amount,
    net_amount

from {{ ref('int_order_items_enriched') }}

where abs(
    gross_amount - (discount_amount + net_amount)
) > 0.01