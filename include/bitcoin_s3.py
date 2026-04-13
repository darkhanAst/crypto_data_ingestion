import pandas as pd
from datetime import date, datetime, timedelta
import pyarrow as pa
import pyarrow.parquet as pq
import s3fs

BUCKET = "s3://aws-public-blockchain/v1.0/btc"

fs = s3fs.S3FileSystem(anon=True)




def read_blocks(date: str):
    base_path = f"aws-public-blockchain/v1.0/btc/blocks/date={date}"

    files = fs.ls(base_path)
    
    if not files:
        print(f"Файлы не найдены для даты {date}")
        return pd.DataFrame()
    
    print(f"Найдено файлов: {len(files)}")
    

    dfs = []
    for i, file_path in enumerate(files, 1):
        try:
            with fs.open(file_path, 'rb') as f:
                df = pd.read_parquet(f, engine='pyarrow')
                dfs.append(df)
            print(f"File read {i}/{len(files)}: {file_path.split('/')[-1]}")
        except Exception as e:
            print(f"Error reading  {file_path}: {e}")
    

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        return combined_df
    else:
        print("No dataframes to concatenate")
        return pd.DataFrame()


def read_transactions(date: str):
    #date = get_date()
    print("Reading transactions from S3...")
    base_path = f"{BUCKET}/transactions/date={date}/"
    files = fs.ls(base_path)
    
    if not files:
        print(f"Файлы не найдены для даты {date}")
        return pd.DataFrame()
    
    print(f"Найдено файлов: {len(files)}")
    

    dfs = []
    for i, file_path in enumerate(files, 1):
        try:
            with fs.open(file_path, 'rb') as f:
                df = pd.read_parquet(f, engine='pyarrow')
                dfs.append(df)
            print(f"File read {i}/{len(files)}: {file_path.split('/')[-1]}")
        except Exception as e:
            print(f"Error reading  {file_path}: {e}")
    

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        return combined_df
    else:
        print("No dataframes to concatenate")
        return pd.DataFrame()


