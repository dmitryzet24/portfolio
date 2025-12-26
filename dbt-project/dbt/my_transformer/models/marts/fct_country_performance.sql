{{ config(materialized="table") }}

with transactions as(
    select * from {{ ref("stg_google_transactions") }}
)

select
    country,
    count(visit_id) as total_transactions,
    sum(transactions) as total_tramsactions,
    round(sum(revenue_usd)::numeric, 2) as total_revenue,
    round(avg(revenue_usd)::numeric, 2) as avg_check
from transactions
group by 1
order by total_revenue desc
