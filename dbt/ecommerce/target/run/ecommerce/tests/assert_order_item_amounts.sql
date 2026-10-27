
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select
    order_item_id,
    gross_amount,
    discount_amount,
    net_amount

from "ecommerce"."analytics_intermediate"."int_order_items_enriched"

where abs(
    gross_amount - (discount_amount + net_amount)
) > 0.01
  
  
      
    ) dbt_internal_test