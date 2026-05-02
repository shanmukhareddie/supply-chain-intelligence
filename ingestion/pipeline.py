from ingestion.load.postgres import save_to_db, get_latest_date
from ingestion.db_connection import get_engine
from config import config
from logger import logger
from datetime import timedelta
from ingestion.sources.fred import fetch_fred_data

engine = get_engine()

for code in config.commodity_codes:
    try:
        latest_date = get_latest_date("commodities_prices", code, engine)
        if latest_date:
            latest_date = latest_date + timedelta(days=1)
        print(f"{code} latest date: {latest_date}")
        data = fetch_fred_data(code, start_date=latest_date)
        print(f"{code} fetched rows: {len(data)}")
        save_to_db(data, "commodities_prices")
    except Exception as e:
        logger.error(f"Failed for {code}: {e}")