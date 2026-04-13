select *
from {{ ref('btc_blocks_daily') }}
where total_transactions < 0
   or blocks_count < 0
   or avg_txs_per_block < 0