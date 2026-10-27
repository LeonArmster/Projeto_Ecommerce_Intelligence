
  create view "ecommerce"."analytics_intermediate"."int_order_items_aggregated__dbt_tmp"
    
    
  as (
    with order_items as (

    select *
    from "ecommerce"."analytics_intermediate"."int_order_items_enriched"

),

aggregated as (

    select
        order_id,

        count(*) as item_count,
        count(distinct product_id) as distinct_products,
        sum(quantity) as total_quantity,

        sum(gross_amount) as gross_amount,
        sum(discount_amount) as discount_amount,
        sum(net_amount) as net_amount,

        sum(
            weight_kg * quantity
        ) as total_weight_kg

    from order_items

    group by order_id

)

select *
from aggregated
  );