
      update "ecommerce"."snapshots"."snapshot_orders_status"
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "snapshot_orders_status__dbt_tmp025419894709" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = "ecommerce"."snapshots"."snapshot_orders_status".dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and "ecommerce"."snapshots"."snapshot_orders_status".dbt_valid_to is null;
      


    insert into "ecommerce"."snapshots"."snapshot_orders_status" ("order_id", "order_status", "shipping_type", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."order_id",DBT_INTERNAL_SOURCE."order_status",DBT_INTERNAL_SOURCE."shipping_type",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "snapshot_orders_status__dbt_tmp025419894709" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;

  