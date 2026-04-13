with base as (
    select *
    from {{ source('btc_stage', 'transactions') }}
),

final as(
    select
        date,
        count(*) as tx_count,
        sum(size) as total_tx_size,
        sum(output_value) as total_output_value,
        sum(input_value) as total_input_value,
        sum(fee) as total_fees,
        avg(fee) as avg_fee,
        avg(output_value) as avg_tx_value

    from base
    group by date
)

select *  
  from final


