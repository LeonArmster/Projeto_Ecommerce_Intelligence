
    
    

select
    shipment_id as unique_field,
    count(*) as n_records

from "ecommerce"."analytics_intermediate"."int_shipments_enriched"
where shipment_id is not null
group by shipment_id
having count(*) > 1


