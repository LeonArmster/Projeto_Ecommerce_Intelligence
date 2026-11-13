
with history as (

    select
        customer_id,
        customer_version_key,
        valid_from,
        valid_to,
        is_current,

        lead(valid_from) over (
            partition by customer_id
            order by valid_from, customer_version_key
        ) as next_valid_from

    from {{ ref('dim_customers_history') }}

)

select *
from history

where
    valid_to < valid_from

    or (
        valid_to is not null
        and next_valid_from is not null
        and valid_to > next_valid_from
    )

    or (
        is_current = true
        and valid_to is not null
    )

    or (
        is_current = false
        and valid_to is null
    )
