
  create view "ecommerce"."analytics_intermediate"."int_orders_customer_history__dbt_tmp"
    
    
  as (
    

with orders as (

    select
        order_id,
        customer_id,
        order_at,
        order_status

    from "ecommerce"."analytics_marts"."fct_orders"

),

customer_history as (

    select
        customer_version_key,
        customer_id,
        state,
        valid_from,
        valid_to

    from "ecommerce"."analytics_marts"."dim_customers_history"

),

historical_join as (

    select
        o.order_id,
        o.customer_id,
        o.order_at,
        o.order_status,
        h.customer_version_key,
        h.state as historical_state,
        h.valid_from as customer_valid_from,
        h.valid_to as customer_valid_to,

        case
            when h.customer_version_key is not null
                then true
            else false
        end as has_historical_match

    from orders o

    left join customer_history h
        on o.customer_id = h.customer_id
       and o.order_at >= h.valid_from
       and (
           o.order_at < h.valid_to
           or h.valid_to is null
       )

)

select *
from historical_join
  );