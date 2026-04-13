from cosmos.config import ProfileConfig


clickhouse_db = ProfileConfig(
    profile_name="dbt_crypto_analytics",
    target_name="dev",
    profiles_yml_filepath="/usr/local/airflow/dbt/dbt_crypto_analytics/profiles.yml",
)
