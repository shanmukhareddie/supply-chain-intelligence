# Supply Chain Intelligence Platform

![CI](https://github.com/shanmukhareddie/supply-chain-intelligence/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An end-to-end supply chain analytics platform that ingests real global commodity and trade data, detects market disruptions, forecasts prices 90 days ahead, and surfaces executive-level risk indicators through a live interactive dashboard.

**[Live Dashboard](https://shanmukhareddie-supply-chain.streamlit.app)**
**[GitHub](https://github.com/shanmukhareddie/supply-chain-intelligence)**

---

## The Problem

Supply chain disruptions cost global businesses over $4 trillion annually. Most organisations react after the damage is done. This platform uses real commodity prices, freight indices, and global trade flows to proactively surface risk — before it hits the bottom line.

---

## What It Does

- Ingests real data daily from FRED and World Bank APIs — oil, gas, wheat, coal, gold prices and trade flows across 6 countries
- Detects anomalies using statistical methods on commodity prices and Isolation Forest on Baltic Dry shipping indices
- Forecasts prices 90 days ahead using Facebook Prophet time series models
- Calculates 5 supply chain KPIs — price volatility, freight trend, trade growth, risk score, anomaly rate
- Simulates disruption scenarios — interactive what-if analysis for oil price shocks and their freight cost impact
- Runs automatically every day via GitHub Actions with incremental loading and duplicate prevention

---

## Architecture

```
FRED API + World Bank API
        |
        v
[ingestion/sources]     -- fetch, parse, validate per source
        |
        v
[ingestion/load]        -- incremental upsert to PostgreSQL
        |
        v
[Supabase PostgreSQL]   -- commodities_prices
                        -- freight_indices
                        -- trade_flows
        |
        v
[ingestion/models]      -- Prophet forecasting
                        -- Isolation Forest anomaly detection
                        -- Correlation analysis
        |
        v
[ingestion/analysis]    -- 5 KPI calculations
                        -- Scenario modelling
        |
        v
[dashboard/app.py]      -- Streamlit live dashboard
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Database | PostgreSQL via Supabase |
| ORM | SQLAlchemy 2.0 |
| Pipeline | Custom ETL + GitHub Actions CI/CD |
| Forecasting | Facebook Prophet |
| Anomaly Detection | Isolation Forest (scikit-learn) |
| Dashboard | Streamlit |
| Testing | pytest + pytest-cov |

---

## Key Results

| Metric | Value |
|---|---|
| Oil price anomalies detected | 1,242 |
| Freight anomalies detected | 337 |
| Oil-freight correlation | 0.364 |
| Forecast horizon | 90 days |
| Commodities tracked | 5 |
| Countries tracked | 6 |

---

## Data Sources

| Source | Data | Frequency |
|---|---|---|
| [FRED](https://fred.stlouisfed.org) | Oil, gas, wheat, coal, gold prices + Baltic Dry Index | Daily |
| [World Bank](https://data.worldbank.org) | Merchandise imports/exports by country | Annual |

---

## Getting Started

```bash
# Clone
git clone https://github.com/shanmukhareddie/supply-chain-intelligence.git
cd supply-chain-intelligence

# Virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your DATABASE_URL and FRED_API_KEY to .env

# Verify setup
pytest tests/ -v

# Run pipeline
python -m ingestion.pipeline

# Launch dashboard
streamlit run dashboard/app.py
```

---

## Project Structure

```
supply-chain-intelligence/
├── ingestion/
│   ├── sources/        # FRED and World Bank API clients
│   ├── load/           # Database upsert logic
│   ├── models/         # Prophet forecasting + anomaly detection
│   ├── analysis/       # KPI calculations + scenario modelling
│   └── pipeline.py     # Main orchestration
├── dashboard/
│   └── app.py          # Streamlit dashboard
├── tests/              # pytest test suite
├── docs/
│   └── model_metrics.csv
├── .github/workflows/  # CI/CD pipeline
└── schema.sql          # Database schema
```

---

## License

MIT — Shanmukha Reddy Gangula
