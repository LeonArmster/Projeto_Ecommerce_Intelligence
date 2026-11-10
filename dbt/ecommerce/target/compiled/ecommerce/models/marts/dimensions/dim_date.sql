

with date_spine as (

    select
        generate_series(
            '2022-01-01'::date,
            '2030-12-31'::date,
            interval '1 day'
        )::date as full_date

),

final as (

    select
        to_char(full_date, 'YYYYMMDD')::integer
            as date_key,

        full_date,

        extract(year from full_date)::integer
            as year,

        extract(quarter from full_date)::integer
            as quarter,

        extract(month from full_date)::integer
            as month,

        trim(to_char(full_date, 'Month'))
            as month_name,

        extract(day from full_date)::integer
            as day_of_month,

        extract(isodow from full_date)::integer
            as day_of_week_iso,

        extract(week from full_date)::integer
            as week_of_year_iso,

        extract(isoyear from full_date)::integer
            as iso_year,

        (extract(isodow from full_date) in (6, 7))
            as is_weekend

    from date_spine

)

select *
from final