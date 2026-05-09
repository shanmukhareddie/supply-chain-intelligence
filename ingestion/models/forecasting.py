import pandas as pd
from prophet import Prophet
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from config import config

def load_commodity_data(commodity, engine):
    query = f"SELECT date, price_usd FROM commodities_prices WHERE commodity = '{commodity}' ORDER BY date"
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def load_freight_data(engine):
    query = "SELECT date, value FROM freight_indices ORDER BY date"
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def detect_anomalies(df):
    df = df.copy()
    df['rolling_mean'] = df['price_usd'].rolling(window=30).mean()
    df['rolling_std'] = df['price_usd'].rolling(window=30).std()
    
    upper = df['rolling_mean'] + 2 * df['rolling_std']
    lower = df['rolling_mean'] - 2 * df['rolling_std']
    
    anomalies = df[(df['price_usd'] > upper) | (df['price_usd'] < lower)]
    
    return anomalies

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

def detect_freight_anomalies(df):
    df = df.copy()
    model = IsolationForest(contamination=0.05)
    model.fit(df[['value']])
    df['anomaly'] = model.predict(df[['value']])
    return df[df['anomaly'] == -1]


def correlation_analysis(engine):
    df1 = load_commodity_data("DCOILBRENTEU", engine)
    df2 = load_freight_data(engine)
    merged = pd.merge(df1, df2, on='date', how='inner')
    correlation = merged['price_usd'].corr(merged['value'])
    return correlation

def save_model_metrics(engine):
    metrics = {'metric': [], 'value': []}
    
    # anomalies for each commodity
    for code in config.commodity_names:
        df = load_commodity_data(code, engine)
        anomalies = detect_anomalies(df)
        name = config.commodity_names.get(code, code)
        metrics['metric'].append(f'{name}_anomalies')
        metrics['value'].append(len(anomalies))
    
    # freight anomalies
    df_freight = load_freight_data(engine)
    freight_anom = detect_freight_anomalies(df_freight)
    metrics['metric'].append('freight_anomalies')
    metrics['value'].append(len(freight_anom))
    
    # correlation
    corr = correlation_analysis(engine)
    metrics['metric'].append('oil_freight_correlation')
    metrics['value'].append(round(corr, 3))
    
    # forecast horizon
    metrics['metric'].append('forecast_horizon_days')
    metrics['value'].append(90)
    
    df = pd.DataFrame(metrics)
    df.to_csv('docs/model_metrics.csv', index=False)
    print("Metrics saved to docs/model_metrics.csv")


if __name__ == "__main__":
    from ingestion.db_connection import get_engine
    engine = get_engine()
    df = load_commodity_data("DCOILBRENTEU", engine)
    forecast = forecast_commmodities(df)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10))

    df2 = load_commodity_data("DCOILBRENTEU", engine)
    anomalies = detect_anomalies(df2)
    print(f"\nTotal anomalies found: {len(anomalies)}")
    print(anomalies[['date', 'price_usd', 'rolling_mean']].head(10))

    # Test freight anomalies
    df_freight = load_freight_data(engine)
    anomalies = detect_freight_anomalies(df_freight)
    print(f"Freight anomalies found: {len(anomalies)}")
    print(anomalies[['date', 'value']].head(10))

    correlation = correlation_analysis(engine)
    print(f"\nOil vs Freight correlation: {correlation:.3f}")

    save_model_metrics(engine)


'''
ds         → the date
yhat       → predicted price (best guess)
yhat_lower → lower bound (pessimistic scenario)
yhat_upper → upper bound (optimistic scenario)
'''