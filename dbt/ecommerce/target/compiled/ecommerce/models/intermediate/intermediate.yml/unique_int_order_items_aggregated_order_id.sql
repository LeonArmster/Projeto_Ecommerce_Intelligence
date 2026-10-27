
    
    

select
    order_id as unique_field,
    count(*) as n_records

from "ecommerce"."analytics_intermediate"."int_order_items_aggregated"
where order_id is not null
group by order_id
having count(*) > 1


