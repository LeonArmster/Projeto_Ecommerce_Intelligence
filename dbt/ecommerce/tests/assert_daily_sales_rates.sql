select
    order_date,
    cancellation_rate,
    delay_rate,
    review_rate

from {{ ref('fct_daily_sales') }}

where
       cancellation_rate not between 0 and 1

    or delay_rate not between 0 and 1

    or review_rate not between 0 and 1