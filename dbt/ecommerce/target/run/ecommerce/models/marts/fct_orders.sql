
      -- back compat for old kwarg name
  
  
        
            
            
            
            
        
    

    

    merge into "ecommerce"."analytics_marts"."fct_orders" as DBT_INTERNAL_DEST
        using "fct_orders__dbt_tmp024732078942" as DBT_INTERNAL_SOURCE
        on ((DBT_INTERNAL_SOURCE.order_id = DBT_INTERNAL_DEST.order_id))

    
    when matched then update set
        "order_id" = DBT_INTERNAL_SOURCE."order_id","customer_id" = DBT_INTERNAL_SOURCE."customer_id","order_at" = DBT_INTERNAL_SOURCE."order_at","order_status" = DBT_INTERNAL_SOURCE."order_status","shipping_type" = DBT_INTERNAL_SOURCE."shipping_type","customer_state" = DBT_INTERNAL_SOURCE."customer_state","customer_birth_date" = DBT_INTERNAL_SOURCE."customer_birth_date","customer_created_at" = DBT_INTERNAL_SOURCE."customer_created_at","item_count" = DBT_INTERNAL_SOURCE."item_count","distinct_products" = DBT_INTERNAL_SOURCE."distinct_products","total_quantity" = DBT_INTERNAL_SOURCE."total_quantity","gross_amount" = DBT_INTERNAL_SOURCE."gross_amount","discount_amount" = DBT_INTERNAL_SOURCE."discount_amount","net_amount" = DBT_INTERNAL_SOURCE."net_amount","total_weight_kg" = DBT_INTERNAL_SOURCE."total_weight_kg","payment_id" = DBT_INTERNAL_SOURCE."payment_id","payment_method" = DBT_INTERNAL_SOURCE."payment_method","payment_amount" = DBT_INTERNAL_SOURCE."payment_amount","installments" = DBT_INTERNAL_SOURCE."installments","payment_status" = DBT_INTERNAL_SOURCE."payment_status","paid_at" = DBT_INTERNAL_SOURCE."paid_at","shipment_id" = DBT_INTERNAL_SOURCE."shipment_id","shipped_at" = DBT_INTERNAL_SOURCE."shipped_at","estimated_delivery_at" = DBT_INTERNAL_SOURCE."estimated_delivery_at","delivered_at" = DBT_INTERNAL_SOURCE."delivered_at","delivery_duration" = DBT_INTERNAL_SOURCE."delivery_duration","is_delayed" = DBT_INTERNAL_SOURCE."is_delayed","review_id" = DBT_INTERNAL_SOURCE."review_id","rating" = DBT_INTERNAL_SOURCE."rating","reviewed_at" = DBT_INTERNAL_SOURCE."reviewed_at"
    

    when not matched then insert
        ("order_id", "customer_id", "order_at", "order_status", "shipping_type", "customer_state", "customer_birth_date", "customer_created_at", "item_count", "distinct_products", "total_quantity", "gross_amount", "discount_amount", "net_amount", "total_weight_kg", "payment_id", "payment_method", "payment_amount", "installments", "payment_status", "paid_at", "shipment_id", "shipped_at", "estimated_delivery_at", "delivered_at", "delivery_duration", "is_delayed", "review_id", "rating", "reviewed_at")
    values
        ("order_id", "customer_id", "order_at", "order_status", "shipping_type", "customer_state", "customer_birth_date", "customer_created_at", "item_count", "distinct_products", "total_quantity", "gross_amount", "discount_amount", "net_amount", "total_weight_kg", "payment_id", "payment_method", "payment_amount", "installments", "payment_status", "paid_at", "shipment_id", "shipped_at", "estimated_delivery_at", "delivered_at", "delivery_duration", "is_delayed", "review_id", "rating", "reviewed_at")


  