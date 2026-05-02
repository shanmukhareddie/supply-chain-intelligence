# Supply Chain Intelligence Platform

![CI](https://github.com/shanmukhareddie/supply-chain-intelligence/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An end-to-end supply chain analytics platform that ingests real global trade data, detects disruptions, forecasts demand, and surfaces business recommendations through an interactive dashboard.

---

## Problem

Supply chain disruptions cost global businesses trillions annually. Most organisations react to disruptions after they happen. This platform uses historical trade, commodity, and freight data to **proactively detect risk** and **forecast demand changes** before they impact operations.

---

## Architecture

```
Raw APIs / CSVs (World Bank, UN Comtrade, FRED)
        │
        ▼
[ingestion/sources]   — fetch & parse per-source
        │
        ▼
[ingestion/transform] — clean, validate, standardise
        │
        ▼
[PostgreSQL]          — commodities_prices
                      — freight_indices
                      — trade_flows
                      — pipeline_log
        │
        ▼
[ML models]           — demand forecasting (ARIMA/Prophet)
                      — anomaly detection (Isolation Forest)
        │
        ▼
[Dashboard]           — Streamlit interactive UI (live URL)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Database | PostgreSQL (Supabase) |
| ORM | SQLAlchemy 2.0 |
| Pipeline | Custom ETL + GitHub Actions schedule |
| ML | scikit-learn, statsmodels, Prophet |
| Dashboard | Streamlit + Plotly |
| Testing | pytest + pytest-cov |
| CI/CD | GitHub Actions |
| Containerisation | Docker + docker-compose |

---

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL (or a free [Supabase](https://supabase.com) account)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/supply-chain-intelligence.git
cd supply-chain-intelligence

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# 5. Verify your setup
pytest tests/test_day1_setup.py -v
```

### Run the pipeline

```bash
python ingestion/pipeline.py
```

---

## Data Sources

| Source | Data | Update frequency |
|---|---|---|
| [World Bank API](https://data.worldbank.org) | Commodity prices (coal, oil, wheat) | Monthly |
| [UN Comtrade](https://comtradeplus.un.org) | Bilateral trade flows by commodity | Annual |
| [FRED](https://fred.stlouisfed.org) | Baltic Dry Index (freight costs) | Daily |


## License

MIT
