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



freight_codes = ["NASDAQB4040GI"]

for code in freight_codes:
    try:
        latest_date = get_latest_date("freight_indices", code, engine, column="index_name")
        if latest_date:
            latest_date = latest_date + timedelta(days=1)
        data = fetch_fred_data(code, start_date=latest_date)
        data = data.rename(columns={
            "price_usd": "value",
            "commodity": "index_name"
        })
        save_to_db(data, "freight_indices")
        logger.info(f"Processed freight index {code}")
    except Exception as e:
        logger.error(f"Failed freight {code}: {e}")