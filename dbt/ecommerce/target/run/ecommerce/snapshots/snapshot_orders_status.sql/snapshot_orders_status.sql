
      
  
    

  create  table "ecommerce"."snapshots"."snapshot_orders_status"
  
  
    as
  
  (
    
    

    select *,
        md5(coalesce(cast(order_id as varchar ), '')
         || '|' || coalesce(cast(now()::timestamp without time zone as varchar ), '')
        ) as dbt_scd_id,
        now()::timestamp without time zone as dbt_updated_at,
        now()::timestamp without time zone as dbt_valid_from,
        
  
  coalesce(nullif(now()::timestamp without time zone, now()::timestamp without time zone), null)
  as dbt_valid_to
from (
        



select
    order_id,
    order_status,
    shipping_type

from "ecommerce"."analytics_staging"."stg_orders"

    ) sbq



  );
  
  