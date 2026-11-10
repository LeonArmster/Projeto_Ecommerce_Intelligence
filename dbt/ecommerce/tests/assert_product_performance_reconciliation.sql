
with fact_metrics as (

    select
        product_id,

        count(distinct order_id) filter (
            where order_status = 'completed'
        ) as completed_orders,

        coalesce(
            sum(quantity) filter (
                where order_status = 'completed'
            ), 0
        ) as units_sold,

        coalesce(
            sum(net_amount) filter (
                where order_status = 'completed'
            ), 0
        ) as net_revenue

    from {{ ref('fct_order_items') }}
    group by product_id

),

mart_metrics as (

    select
        product_id,
        completed_orders,
        units_sold,
        net_revenue

    from {{ ref('mart_product_performance') }}

)

select
    coalesce(f.product_id, m.product_id) as product_id,

    f.completed_orders as expected_orders,
    m.completed_orders as actual_orders,

    f.units_sold as expected_units,
    m.units_sold as actual_units,

    f.net_revenue as expected_revenue,
    m.net_revenue as actual_revenue

from fact_metrics f

full outer join mart_metrics m
    on f.product_id = m.product_id

where
    m.product_id is null

    or coalesce(f.completed_orders, 0)
        <> coalesce(m.completed_orders, 0)

    or coalesce(f.units_sold, 0)
        <> coalesce(m.units_sold, 0)

    or abs(
        coalesce(f.net_revenue, 0)
        - coalesce(m.net_revenue, 0)
    ) > 0.01
