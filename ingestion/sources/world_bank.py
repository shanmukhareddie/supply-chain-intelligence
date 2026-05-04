import requests
import pandas as pd
from logger import logger
from ingestion.db_connection import get_engine
from ingestion.load.postgres import save_to_db

def world_bank_data(country, indicator):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&date=2015:2024&per_page=500"
    response = requests.get(url)
    data = response.json()

    records = data[1]
    df = pd.DataFrame([{
        "date": r["date"],
        "value": r["value"],
        "country": r["country"]["value"],
        "indicator": r["indicator"]["value"]
    } for r in records if r["value"] is not None])

    return df


def world_bank_pipeline():
    engine = get_engine()
    
    countries = ["US", "CN", "DE", "JP", "GB", "IN"]
    indicators = {
        "TM.VAL.MRCH.WL.CD": "import",
        "TX.VAL.MRCH.WL.CD": "export"
    }

    for country in countries:
        for indicator, trade_flow in indicators.items():
            try:
                df = world_bank_data(country, indicator)
                df['trade_flow'] = trade_flow
                df['origin_country'] = country
                df['destination_country'] = "World"
                df = df.rename(columns={"value": "trade_value_usd", "date": "year"})
                df['year'] = df['year'].astype(int)  
                df['commodity'] = "merchandise"       # add missing commodity column
                df['source'] = "World Bank"           # add source
                df = df[['year', 'origin_country', 'destination_country','trade_value_usd', 'trade_flow', 'commodity', 'source']]
                save_to_db(df, "trade_flows")
                logger.info(f"Saved {len(df)} rows for {country} {trade_flow}")
            except Exception as e:
                logger.error(f"Failed for {country} {indicator}: {e}")


if __name__ == "__main__":
    world_bank_pipeline()