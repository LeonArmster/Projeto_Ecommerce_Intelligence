
  create view "ecommerce"."analytics_staging"."stg_products__dbt_tmp"
    
    
  as (
    with source as (

    select *
    from "ecommerce"."raw"."products"

),

renamed as (

    select
        product_id,
        category,
        brand,
        base_price,
        weight_kg

    from source

)

select *
from renamed
  );