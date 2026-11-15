
      update "ecommerce"."snapshots"."snapshot_customers"
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "snapshot_customers__dbt_tmp041121601854" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = "ecommerce"."snapshots"."snapshot_customers".dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and "ecommerce"."snapshots"."snapshot_customers".dbt_valid_to is null;
      


    insert into "ecommerce"."snapshots"."snapshot_customers" ("customer_id", "birth_date", "state", "created_at", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."customer_id",DBT_INTERNAL_SOURCE."birth_date",DBT_INTERNAL_SOURCE."state",DBT_INTERNAL_SOURCE."created_at",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "snapshot_customers__dbt_tmp041121601854" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;

  