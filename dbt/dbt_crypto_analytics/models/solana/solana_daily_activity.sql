with base as (
    select *
    from {{ source('solana_stage', 'solana_blocks') }}
),

final as ( 
    select
        toDate(block_time) as date,

        count(*) as blocks_count,
        sum(tx_count) as total_transactions,
        avg(tx_count) as avg_txs_per_block,

        max(tx_count) as max_txs_in_block

    from base
    group by date

)
select *  
  from final
