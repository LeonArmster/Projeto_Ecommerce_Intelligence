
  
    

  create  table "ecommerce"."analytics"."dim_products__dbt_tmp"
  
  
    as
  
  (
    

with products as (

    select
        product_id,
        category,
        brand,
        base_price,
        weight_kg

    from "ecommerce"."analytics_staging"."stg_products"

),

final as (

    select
        product_id,
        category,
        brand,
        base_price,
        weight_kg

    from products

)

select *
from final
  );
  