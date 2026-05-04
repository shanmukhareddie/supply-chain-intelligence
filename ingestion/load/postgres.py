from ingestion.db_connection import get_engine
from sqlalchemy import text
from logger import logger
import pandas as pd


def save_to_db(df, table_name):
    if df.empty:
        logger.info(f"No new data for {table_name}")
        return

    engine = get_engine()
    df = df.copy()

    if 'price_usd' in df.columns:
        df['price_usd'] = pd.to_numeric(df['price_usd'], errors='coerce')
        df = df.dropna(subset=['price_usd'])

    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
            chunksize=500,
            method="multi"
        )
        logger.info(f"Saved {len(df)} new rows to {table_name}")
    except Exception:
        # filter out duplicates then retry once
        logger.info(f"Duplicates detected — retrying {table_name}")
        try:
            df.drop_duplicates().to_sql(
                name=table_name,
                con=engine,
                if_exists="append",
                index=False,
                chunksize=500,
                method="multi"
            )
            logger.info(f"Saved rows to {table_name} after dedup")
        except Exception as e:
            logger.error(f"Failed to save to {table_name}: {e}")

def get_latest_date(table_name, value, engine, column="commodity"):
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT MAX(date) FROM {table_name} WHERE {column} = :value"),
            {"value": value}
        )
        return result.scalar()