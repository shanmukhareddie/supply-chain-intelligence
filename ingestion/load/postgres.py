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
    df['price_usd'] = pd.to_numeric(df['price_usd'], errors='coerce')
    df = df.dropna(subset=['price_usd'])
    
    if df.empty:
        logger.info(f"No new rows to save for {table_name}")
        return

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
        # Insert row by row, skipping duplicates
        saved = 0
        for _, row in df.iterrows():
            try:
                pd.DataFrame([row]).to_sql(
                    name=table_name,
                    con=engine,
                    if_exists="append",
                    index=False
                )
                saved += 1
            except Exception:
                pass
        logger.info(f"Saved {saved} new rows to {table_name} (skipped duplicates)")


def get_latest_date(table_name, commodity, engine):
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT MAX(date) FROM {table_name} WHERE commodity = :commodity"),
            {"commodity": commodity}
        )
        return result.scalar()