
select
    customer_id,
    count(*) as current_versions

from {{ ref('dim_customers_history') }}

where is_current = true

group by customer_id

having count(*) > 1
