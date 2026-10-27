
  create view "ecommerce"."analytics_staging"."stg_orders__dbt_tmp"
    
    
  as (
    with source as (

    select *
    from "ecommerce"."raw"."orders"

),

renamed as (

    select
        order_id,
        customer_id,
        order_date as order_at,
        order_status,
        shipping_type

    from source

)

select *
from renamed
  );