with base as (
    select *
    from {{ source('btc_stage', 'blocks') }}
),

final as (
    select
        date,
        count(*) as blocks_count,
        sum(transaction_count) as total_transactions,
        avg(transaction_count) as avg_txs_per_block,
        avg(size) as avg_block_size,
        avg(weight) as avg_weight,
        avg(difficulty) as avg_difficulty,
        max(number) as max_block_number
    from base
    group by date
)

select * 
  from final

