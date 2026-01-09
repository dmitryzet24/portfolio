{{ config(materialized='view') }}

with raw_data as(
    select * from {{ source('external_source', 'raw_google_transactions') }}
)

select
    "visitId" as visit_id,
    to_timestamp("visitStartTime") as visit_tarted_at,
    cast (date as date) as session_date,
    browser,
    device_type,
    country,
    pageviews,
    transactions,
    revenue_usd
from raw_data
where transactions >=1
