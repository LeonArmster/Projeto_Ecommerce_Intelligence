
  create view "ecommerce"."analytics_staging"."stg_reviews__dbt_tmp"
    
    
  as (
    with source as (

    select *
    from "ecommerce"."raw"."reviews"

),

renamed as (

    select
        review_id,
        order_id,
        rating,
        created_at as reviewed_at

    from source

)

select *
from renamed
  );