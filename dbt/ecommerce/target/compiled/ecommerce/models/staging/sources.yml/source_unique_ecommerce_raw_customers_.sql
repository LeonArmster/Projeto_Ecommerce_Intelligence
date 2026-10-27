
    
    

select
     as unique_field,
    count(*) as n_records

from "ecommerce"."raw"."customers"
where  is not null
group by 
having count(*) > 1


