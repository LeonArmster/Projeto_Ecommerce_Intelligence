{% set reference_date = var('customer_reference_date', run_started_at.strftime('%Y-%m-%d')) %}
-- Return any customer whose repeat-purchase metrics violate the business rules.
select *
from {{ ref('mart_customer_360') }}
where is_repeat_customer is distinct from (completed_orders >= 2)
   or (completed_orders < 2 and days_to_second_purchase is not null)
   or (completed_orders >= 2 and (days_to_second_purchase is null or days_to_second_purchase < 0))
   or (completed_orders = 0 and purchase_frequency_per_month is not null)
   or (completed_orders > 0 and purchase_frequency_per_month is null)
   or (purchase_frequency_per_month < 0)
   or days_since_last_purchase < 0
   or first_purchase_at::date > '{{ reference_date }}'::date
   or last_purchase_at::date > '{{ reference_date }}'::date
