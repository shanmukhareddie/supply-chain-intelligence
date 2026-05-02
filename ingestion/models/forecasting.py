import pandas as pd
from prophet import Prophet
from sklearn.model_selection import train_test_split

def load_commodity_data(commodity, engine):
    query = f"SELECT date, price_usd FROM commodities_prices WHERE commodity = '{commodity}' ORDER BY date"
    df = pd.read_sql(query, engine)
    return df

# def forecast_commmodities(df):
#     df = df.rename(columns={'date': 'ds', 'price_usd': 'y'})
#     split = int(len(df) * 0.8)
#     train_data = df[:split]   # first 80%
#     test_data = df[split:]    # last 20%

#     model = Prophet()          
#     model.fit(train_data)  


#     # predict next 90 days
#     future = model.make_future_dataframe(periods=90)
#     forecast = model.predict(future)

#     return forecast

def forecast_commmodities(df):
    df = df.rename(columns={'date': 'ds', 'price_usd': 'y'})
    
    model = Prophet()
    model.fit(df)  # train on ALL data

    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)

    return forecast

if __name__ == "__main__":
    from ingestion.db_connection import get_engine
    engine = get_engine()
    df = load_commodity_data("DCOILBRENTEU", engine)
    forecast = forecast_commmodities(df)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10))



'''
ds         → the date
yhat       → predicted price (best guess)
yhat_lower → lower bound (pessimistic scenario)
yhat_upper → upper bound (optimistic scenario)
'''