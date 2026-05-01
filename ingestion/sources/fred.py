import requests
import pandas as pd
from config import config

def fetch_fred_data(series_id):
    # Step 1 - build URL
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={config.fred_api_key}&file_type=json"

    # Step 2 - call API
    response = requests.get(url)
    data = response.json()

    # Step 3 - parse into DataFrame
    observations = data["observations"]
    df = pd.DataFrame(observations)

    # Step 4 - clean up
    df = df[["date", "value"]]
    df = df.rename(columns={"value": "price_usd"})
    df = df[df["price_usd"] != "."]
    df["commodity"] = series_id
    df["source"] = "FRED"

    return df

if __name__ == "__main__":
    df = fetch_fred_data("DCOILBRENTEU")
    print(df.head())
    print(f"Total rows: {len(df)}")