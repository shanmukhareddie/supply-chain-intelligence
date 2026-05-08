import pandas as pd
from ingestion.db_connection import get_engine
from ingestion.models.forecasting import (
    load_commodity_data,
    load_freight_data,
    detect_anomalies,
    correlation_analysis
)

def calculate_price_volatility(engine):
    df = load_commodity_data("DCOILBRENTEU", engine)
    data=df.tail(30)        # get last 30 days
    return data['price_usd'].std()      # calculate std deviation

def calculate_freight_trend(engine):
    df = load_freight_data(engine)
    data = df.tail(30)
    first = data['value'].iloc[0]   # first value in the 30 days
    last = data['value'].iloc[-1]   # last value in the 30 days
    return round((last - first) / first * 100, 2)

def calculate_trade_growth(engine):
    query = """
        SELECT year, SUM(trade_value_usd) as trade_sum 
        FROM trade_flows 
        GROUP BY year 
        ORDER BY year
    """
    df = pd.read_sql(query, engine)
    df['growth_pct'] = df['trade_sum'].pct_change() * 100
    return round(df['growth_pct'].iloc[-1], 2)

def calculate_risk_score(engine):
    volatility = calculate_price_volatility(engine)
    correlation = correlation_analysis(engine)
    return round(volatility * abs(correlation), 3)

def calculate_anomaly_rate(engine):
    df = load_commodity_data("DCOILBRENTEU", engine)
    last_90 = df.tail(90)
    anomalies = detect_anomalies(last_90)
    return round(len(anomalies) / len(last_90) * 100, 1)


def scenario_oil_price_shock(engine, shock_pct=20):
    df = load_commodity_data("DCOILBRENTEU", engine)
    current_price = df['price_usd'].iloc[-1]
    correlation = correlation_analysis(engine)
    new_price = current_price * (1 + shock_pct / 100)
    freight_impact = shock_pct * correlation
    return {
        'current_oil_price': round(current_price, 2),
        'shock_percentage': shock_pct,
        'new_oil_price': round(new_price, 2),
        'estimated_freight_impact_pct': round(freight_impact, 2)
    }

if __name__ == "__main__":
    from ingestion.db_connection import get_engine
    engine = get_engine()
    print(f"Price Volatility: {calculate_price_volatility(engine):.2f}")
    print(f"Freight Trend: {calculate_freight_trend(engine):.2f}%")
    print(f"Trade Growth: {calculate_trade_growth(engine):.2f}%")
    print(f"Risk Score: {calculate_risk_score(engine):.3f}")
    print(f"Anomaly Rate: {calculate_anomaly_rate(engine):.1f}%")
    print("\n--- Scenario: 20% oil price shock ---")
    scenario = scenario_oil_price_shock(engine)
    for key, value in scenario.items():
        print(f"{key}: {value}")