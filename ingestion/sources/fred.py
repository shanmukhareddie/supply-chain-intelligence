import requests
import pandas as pd
from config import config



def fetch_fred_data(series_id, start_date=None):
    # Step 1 - build URL
    if start_date:
        observation_start = f"&observation_start={start_date}"
    else:
        observation_start = ""  

    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={config.fred_api_key}&file_type=json{observation_start}"

    # Step 2 - call API
    response = requests.get(url)
    data = response.json()

    if "observations" not in data:
        raise ValueError(f"Invalid response for {series_id}: {data}")

    # Step 3 - parse into DataFrame
    observations = data["observations"]
    if not observations:
        return pd.DataFrame()  # return empty DataFrame
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