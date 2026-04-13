with base as (
    select *
    from {{ source('solana_stage', 'solana_performance') }}
),

final as (

    select
        toDate(ts) as date,

        avg(num_transactions / nullif(sample_period, 0)) as avg_tps,
        max(num_transactions / nullif(sample_period, 0)) as peak_tps,

        sum(num_transactions) as total_transactions

    from base
    group by date
)

select *  
  from final



