-- Supply Chain Intelligence — Database Schema

CREATE TABLE commodities_prices (
    id            SERIAL PRIMARY KEY,
    commodity     VARCHAR(100) NOT NULL,
    price_usd     NUMERIC(12,4) NOT NULL,
    unit          VARCHAR(50),
    date          DATE NOT NULL,
    source        VARCHAR(50),
    ingested_at   TIMESTAMP DEFAULT NOW()
);


CREATE TABLE freight_indices (
    id            SERIAL PRIMARY KEY,
    index_name    VARCHAR(100) NOT NULL,
    value         NUMERIC(12,4) NOT NULL,
    date          DATE NOT NULL,
    source        VARCHAR(50),
    ingested_at   TIMESTAMP DEFAULT NOW()
);


CREATE TABLE trade_flows (
    id                  SERIAL PRIMARY KEY,
    origin_country      VARCHAR(100) NOT NULL,
    destination_country VARCHAR(100) NOT NULL,
    commodity           VARCHAR(100) NOT NULL,
    trade_value_usd     NUMERIC(15,2),
    quantity            NUMERIC(15,4),
    trade_flow          VARCHAR(10) CHECK (trade_flow IN ('import','export')),
    year                INTEGER NOT NULL,
    source              VARCHAR(50),
    ingested_at         TIMESTAMP DEFAULT NOW()
);

-- Indexes for fast querying
CREATE INDEX idx_commodity_date
    ON commodities_prices(commodity, date);

CREATE INDEX  idx_freight_date
    ON freight_indices(index_name, date);

CREATE INDEX  idx_trade_country
    ON trade_flows(origin_country, destination_country, year);