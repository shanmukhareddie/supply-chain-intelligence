import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from ingestion.db_connection import get_engine
from ingestion.analysis.kpis import (
    calculate_price_volatility,
    calculate_freight_trend,
    calculate_trade_growth,
    calculate_risk_score,
    calculate_anomaly_rate,
    scenario_oil_price_shock
)
from ingestion.models.forecasting import (
    load_commodity_data,
    load_freight_data,
    forecast_commmodities,
    detect_anomalies,
    detect_freight_anomalies
)

# ── Page config 
st.set_page_config(
    page_title="Supply Chain Intelligence",
    page_icon="🌐",
    layout="wide"
)

# ── Custom CSS 
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 1.5rem; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #2a2d3e);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #3a3d4e;
    }
    h1 { color: #ffffff; font-size: 2rem !important; }
    h2, h3 { color: #e0e0e0; }
    .stMetric label { color: #9ca3af !important; font-size: 0.8rem !important; }
    .stMetric value { color: #ffffff !important; }
    div[data-testid="stHorizontalBlock"] {
        background: #1e2130;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #2a2d3e;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header 
st.markdown("# 🌐 Supply Chain Intelligence Platform")
st.markdown("**Real-time supply chain risk monitoring** · Powered by FRED & World Bank APIs · Data: Oil, Gas, Wheat, Coal, Gold + Freight")
st.divider()

# ── Engine 
@st.cache_resource
def get_cached_engine():
    return get_engine()

engine = get_cached_engine()

import os
st.write(f"DB URL starts with: {os.getenv('DATABASE_URL', 'NOT FOUND')[:30]}")

# ── KPIs 
st.subheader("📊 Key Performance Indicators")

@st.cache_data(ttl=3600)
def load_kpis(_engine):
    return {
        'volatility': calculate_price_volatility(_engine),
        'freight': calculate_freight_trend(_engine),
        'trade': calculate_trade_growth(_engine),
        'risk': calculate_risk_score(_engine),
        'anomaly': calculate_anomaly_rate(_engine)
    }

kpis = load_kpis(engine)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🛢️ Price Volatility", f"${kpis['volatility']:.2f}", help="30-day std deviation of Brent Crude oil price")
col2.metric("🚢 Freight Trend", f"{kpis['freight']:.2f}%", help="Baltic Dry Index % change over last 30 days")
col3.metric("🌍 Trade Growth", f"{kpis['trade']:.2f}%", delta=f"{kpis['trade']:.2f}%", help="Year-over-year global trade value change")
col4.metric("⚠️ Risk Score", f"{kpis['risk']:.2f}", help="Combined oil volatility × freight correlation")
col5.metric("🔴 Anomaly Rate", f"{kpis['anomaly']:.1f}%", help="% of last 90 days with abnormal oil prices")

st.divider()

# ── Forecast 
st.subheader("📈 90-Day Oil Price Forecast")

@st.cache_data(ttl=3600)
def load_forecast(_engine):
    df = load_commodity_data("DCOILBRENTEU", _engine)
    forecast = forecast_commmodities(df)
    actual = df.tail(365).copy()
    actual['date'] = pd.to_datetime(actual['date'])
    forecast['ds'] = pd.to_datetime(forecast['ds'])
    future = forecast[forecast['ds'] > actual['date'].max()][['ds', 'yhat']].copy()
    future = future.rename(columns={'ds': 'date', 'yhat': 'price_usd'}).set_index('date')
    actual_chart = actual[['date', 'price_usd']].set_index('date')
    return actual_chart, future

actual_chart, future_chart = load_forecast(engine)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("**Actual Prices — Last 365 Days**")
    st.line_chart(actual_chart, color="#3b82f6")
with col_b:
    st.markdown("**Forecast — Next 90 Days**")
    st.line_chart(future_chart, color="#10b981")

st.divider()

# ── Anomalies 
st.subheader("🔍 Anomaly Detection")

@st.cache_data(ttl=3600)
def load_anomalies(_engine):
    df_oil = load_commodity_data("DCOILBRENTEU", _engine)
    df_freight = load_freight_data(_engine)
    oil_anom = detect_anomalies(df_oil)
    freight_anom = detect_freight_anomalies(df_freight)
    return oil_anom, freight_anom

oil_anom, freight_anom = load_anomalies(engine)

col_c, col_d = st.columns(2)
with col_c:
    st.markdown(f"**Oil Price Anomalies — {len(oil_anom)} detected**")
    st.dataframe(
        oil_anom[['date', 'price_usd', 'rolling_mean']].tail(20).reset_index(drop=True),
        use_container_width=True
    )
with col_d:
    st.markdown(f"**Freight Anomalies — {len(freight_anom)} detected**")
    st.dataframe(
        freight_anom[['date', 'value']].tail(20).reset_index(drop=True),
        use_container_width=True
    )

st.divider()

# ── Scenario Model 
st.subheader("🎯 Scenario Analysis: Oil Price Shock Simulator")
st.markdown("Simulate the supply chain impact of an oil price shock in real time.")

shock = st.slider("Oil Price Shock (%)", min_value=-30, max_value=50, value=20, step=5)
scenario = scenario_oil_price_shock(engine, shock_pct=shock)

s1, s2, s3, s4 = st.columns(4)
s1.metric("Current Oil Price", f"${scenario['current_oil_price']}")
s2.metric("Shock Applied", f"{scenario['shock_percentage']}%")
s3.metric("New Oil Price", f"${scenario['new_oil_price']}", delta=f"${scenario['new_oil_price'] - scenario['current_oil_price']:.2f}")
s4.metric("Est. Freight Impact", f"{scenario['estimated_freight_impact_pct']}%")

st.divider()

# ── Trade Flows 
st.subheader("🌏 Global Trade Flows")

@st.cache_data(ttl=3600)
def load_trade(_engine):
    query = """
        SELECT origin_country, trade_flow, year,
               ROUND(trade_value_usd / 1000000000, 2) as value_billions
        FROM trade_flows
        ORDER BY year DESC, value_billions DESC
    """
    return pd.read_sql(query, _engine)

trade_df = load_trade(engine)

country_filter = st.selectbox("Filter by country", ["All"] + sorted(trade_df['origin_country'].unique().tolist()))
if country_filter != "All":
    trade_df = trade_df[trade_df['origin_country'] == country_filter]

st.dataframe(trade_df, use_container_width=True)

# ── Footer 
st.divider()
st.markdown("<p style='text-align:center; color:#6b7280; font-size:0.8rem'>Supply Chain Intelligence Platform · Built with Python, Streamlit, Prophet, Supabase · github.com/shanmukhareddie</p>", unsafe_allow_html=True)