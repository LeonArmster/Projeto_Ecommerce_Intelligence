
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        customer_segment as value_field,
        count(*) as n_records

    from "ecommerce"."analytics_marts"."mart_customer_360"
    group by customer_segment

)

select *
from all_values
where value_field not in (
    'no_purchase','future_purchase','new_customer','active_repeat','at_risk','inactive'
)



  
  
      
    ) dbt_internal_test