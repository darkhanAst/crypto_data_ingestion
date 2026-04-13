{{ codegen.generate_source(
    schema_name= 'btc_stage', 
    database_name= 'btc_stage',
    table_names= ['blocks','transactions'],
    include_descriptions= True,
    generate_columns=True,
) }}