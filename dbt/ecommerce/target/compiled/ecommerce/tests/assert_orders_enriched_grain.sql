with staging as (

    select
        count(*) as total_orders

    from "ecommerce"."analytics_staging"."stg_orders"

),

enriched as (

    select
        count(*) as total_orders

    from "ecommerce"."analytics_intermediate"."int_orders_enriched"

)

select
    staging.total_orders as staging_orders,
    enriched.total_orders as enriched_orders

from staging
cross join enriched

where staging.total_orders <> enriched.total_orders