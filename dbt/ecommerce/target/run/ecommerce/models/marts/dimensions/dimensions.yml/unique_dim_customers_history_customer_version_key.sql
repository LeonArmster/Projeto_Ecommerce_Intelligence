
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    customer_version_key as unique_field,
    count(*) as n_records

from "ecommerce"."analytics_marts"."dim_customers_history"
where customer_version_key is not null
group by customer_version_key
having count(*) > 1



  
  
      
    ) dbt_internal_test