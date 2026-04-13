import clickhouse_connect
import os
from datetime import datetime
import pandas as pd


def get_client():
    return clickhouse_connect.get_client(
        host=os.getenv("DBT_ENV_SECRET_HOST"),
        port=8443,
        username=os.getenv("DBT_ENV_SECRET_USER"),
        password=os.getenv("DBT_ENV_SECRET_PASSWORD"),
        secure=True
    )


def insert_slot(slot):
    client = get_client()

    client.insert(
        "solana_stage.solana_slots",
        [[slot]],
        column_names=["slot"]
    )

def insert_performance(samples):
    client = get_client()

    rows = []
    for s in samples:
        rows.append([
            s["slot"],
            s["numTransactions"],
            s["samplePeriodSecs"]
        ])

    client.insert(
        "solana_stage.solana_performance",
        rows,
        column_names=[
            "slot",
            "num_transactions",
            "sample_period"
        ]
    )

def insert_block(block, slot):
    client = get_client()

    if not block:
        return

    block_time = block.get("blockTime")
    tx_count = len(block.get("transactions", []))

    if block_time:
        block_time = datetime.fromtimestamp(block_time)

    rows = [[
        slot,
        block_time,
        tx_count
    ]]

    client.insert(
        "solana_stage.solana_blocks",
        rows,
        column_names=[
            "slot",
            "block_time",
            "tx_count"
        ]
    )




def insert_btc_blocks(df: pd.DataFrame, date: str):
    client = get_client()

    if df.empty:
        print("Empty dataframe, skipping insert")
        return

    column_mapping = {
        "hash": "hash",
        "number": "number",
        "size": "size",
        "stripped_size": "stripped_size",
        "weight": "weight",
        "version": "version",
        "merkle_root": "merkle_root",
        "timestamp": "timestamp",
        "nonce": "nonce",
        "bits": "bits",
        "coinbase_param": "coinbase_param",
        "transaction_count": "transaction_count",
        "mediantime": "mediantime",
        "difficulty": "difficulty",
        "chainwork": "chainwork",
        "previousblockhash": "previousblockhash"
    }

    df = df[[col for col in df.columns if col in column_mapping]]

    df = df.rename(columns=column_mapping)

    df["date"] = date

    df["date"] = pd.to_datetime(df["date"]).dt.date

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    if "mediantime" in df.columns:
        df["mediantime"] = pd.to_datetime(df["mediantime"], errors="coerce")

    numeric_cols = [
        "size", "stripped_size", "weight", "number",
        "nonce", "transaction_count"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "difficulty" in df.columns:
        df["difficulty"] = pd.to_numeric(df["difficulty"], errors="coerce")

    string_cols = [
        "hash", "merkle_root", "bits",
        "coinbase_param", "chainwork", "previousblockhash"
    ]

    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    columns = [
        "date",
        "hash",
        "size",
        "stripped_size",
        "weight",
        "number",
        "version",
        "merkle_root",
        "timestamp",
        "nonce",
        "bits",
        "coinbase_param",
        "transaction_count",
        "mediantime",
        "difficulty",
        "chainwork",
        "previousblockhash"
    ]

    columns = [col for col in columns if col in df.columns]

    df = df[columns]

    rows = df.values.tolist()

    client.insert(
        "btc_stage.blocks",
        rows,
        column_names=columns
    )

    print(f"Inserted {len(rows)} rows into btc_blocks")


def insert_btc_transactions(df, date):

    client = get_client()

    if df.empty:
        print("Empty dataframe, skipping insert")
        return

    column_mapping = {
        "hash": "hash",
        "size": "size",
        "virtual_size": "virtual_size",
        "version": "version",
        "lock_time": "lock_time",
        "block_hash": "block_hash",
        "block_number": "block_number",
        "block_timestamp": "block_timestamp",
        "index": "index",
        "input_count": "input_count",
        "output_count": "output_count",
        "input_value": "input_value",
        "output_value": "output_value",
        "is_coinbase": "is_coinbase",
        "fee": "fee"
    }

    df = df[[col for col in df.columns if col in column_mapping]]

    df = df.rename(columns=column_mapping)

    df["date"] = date


    
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    if "block_timestamp" in df.columns:
        df["block_timestamp"] = pd.to_datetime(df["block_timestamp"], errors="coerce")

    uint_cols = [
        "size", "virtual_size", "version", "lock_time",
        "block_number", "index", "input_count", "output_count"
    ]

    for col in uint_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype("int64")

    float_cols = ["input_value", "output_value", "fee"]

    for col in float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    if "is_coinbase" in df.columns:
        df["is_coinbase"] = df["is_coinbase"].fillna(False).astype(bool)

    string_cols = ["hash", "block_hash"]

    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    columns = [
        "date",
        "hash",
        "size",
        "virtual_size",
        "version",
        "lock_time",
        "block_hash",
        "block_number",
        "block_timestamp",
        "index",
        "input_count",
        "output_count",
        "input_value",
        "output_value",
        "is_coinbase",
        "fee"
    ]

    columns = [col for col in columns if col in df.columns]

    df = df[columns]

    rows = df.values.tolist()

    client.insert(
        "btc_stage.transactions",
        rows,
        column_names=columns
    )

    print(f"Inserted {len(rows)} rows into btc_transactions")