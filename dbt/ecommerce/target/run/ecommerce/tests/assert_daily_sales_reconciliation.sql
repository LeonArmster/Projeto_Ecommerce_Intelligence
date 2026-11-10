
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  with orders_daily as (

    select
        order_at::date as order_date,

        count(*) as total_orders,

        count(*) filter (
            where order_status <> 'cancelled'
        ) as valid_orders,

        count(*) filter (
            where order_status = 'cancelled'
        ) as cancelled_orders,

        sum(
            case
                when order_status <> 'cancelled'
                    then gross_amount
                else 0
            end
        ) as gross_amount,

        sum(
            case
                when order_status <> 'cancelled'
                    then discount_amount
                else 0
            end
        ) as discount_amount,

        sum(
            case
                when order_status <> 'cancelled'
                    then net_amount
                else 0
            end
        ) as net_amount

    from "ecommerce"."analytics_marts"."fct_orders"

    group by 1

),

daily_sales as (

    select
        order_date,
        total_orders,
        valid_orders,
        cancelled_orders,
        gross_amount,
        discount_amount,
        net_amount

    from "ecommerce"."analytics_marts"."fct_daily_sales"

),

reconciliation as (

    select
        coalesce(o.order_date, d.order_date)
            as order_date,

        o.order_date is null as missing_in_orders,
        d.order_date is null as missing_in_daily,

        o.total_orders as orders_count,
        d.total_orders as daily_count,

        o.valid_orders as orders_valid,
        d.valid_orders as daily_valid,

        o.cancelled_orders as orders_cancelled,
        d.cancelled_orders as daily_cancelled,

        o.gross_amount as orders_gross,
        d.gross_amount as daily_gross,

        o.discount_amount as orders_discount,
        d.discount_amount as daily_discount,

        o.net_amount as orders_net,
        d.net_amount as daily_net

    from orders_daily o

    full outer join daily_sales d
        on o.order_date = d.order_date

)

select *
from reconciliation

where
    missing_in_orders
    or missing_in_daily

    or orders_count is distinct from daily_count

    or orders_valid is distinct from daily_valid

    or orders_cancelled is distinct from daily_cancelled

    or abs(
        coalesce(orders_gross, 0)
        - coalesce(daily_gross, 0)
    ) > 0.01

    or abs(
        coalesce(orders_discount, 0)
        - coalesce(daily_discount, 0)
    ) > 0.01

    or abs(
        coalesce(orders_net, 0)
        - coalesce(daily_net, 0)
    ) > 0.01

    or (orders_gross is null) <> (daily_gross is null)
    or (orders_discount is null) <> (daily_discount is null)
    or (orders_net is null) <> (daily_net is null)
  
  
      
    ) dbt_internal_test