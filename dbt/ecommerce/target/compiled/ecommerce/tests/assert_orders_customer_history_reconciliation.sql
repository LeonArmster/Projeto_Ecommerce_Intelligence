with source_orders as (

    select
        count(*) as total_orders
    from "ecommerce"."analytics_marts"."fct_orders"

),

historical_orders as (

    select
        count(*) as total_orders
    from "ecommerce"."analytics_intermediate"."int_orders_customer_history"

)

select
    s.total_orders as source_total,
    h.total_orders as historical_total

from source_orders s
cross join historical_orders h

where s.total_orders <> h.total_orders