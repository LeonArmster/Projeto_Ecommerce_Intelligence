
    
    

with all_values as (

    select
        day_of_week_iso as value_field,
        count(*) as n_records

    from "ecommerce"."analytics_marts"."dim_date"
    group by day_of_week_iso

)

select *
from all_values
where value_field not in (
    '1','2','3','4','5','6','7'
)


