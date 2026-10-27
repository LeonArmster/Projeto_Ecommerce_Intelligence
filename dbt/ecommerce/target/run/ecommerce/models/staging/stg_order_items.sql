
  create view "ecommerce"."analytics_staging"."stg_order_items__dbt_tmp"
    
    
  as (
    with source as (

    select *
    from "ecommerce"."raw"."order_items"

),

renamed as (

    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        discount_pct

    from source

)

select *
from renamed
  );