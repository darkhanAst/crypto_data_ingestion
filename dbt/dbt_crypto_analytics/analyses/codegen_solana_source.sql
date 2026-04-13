{{ codegen.generate_source(
    database_name ='solana_stage',
    schema_name='solana_stage',
    table_names=['solana_blocks', 'solana_performance'],
    generate_columns=True,
    include_descriptions=True
) }}