
-- Companies Table

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    symbol TEXT UNIQUE,
    sector TEXT,
    open REAL,
    current_price REAL,
    previous_close REAL,
    volume NUMERIC,
    average_volume NUMERIC,
    eps_current_year REAL,
    week_52_high REAL,
    week_52_low REAL,
    payout_ratio REAL,
    target_mean_price REAL,
    dividend_rate NUMERIC,
    market_sentiment TEXT
);

-- Financial metrics table

CREATE TABLE IF NOT EXISTS financial_metrics (
    global_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    symbol TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    dividends NUMERIC,
    stock_splits REAL,
    FOREIGN KEY(global_id) REFERENCES companies(id)
    UNIQUE(global_id, date)
);

-- Periodic metrics table

CREATE TABLE IF NOT EXISTS periodic_metrics (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adjusted_close REAL,
    volume NUMERIC,
    dividend_amt NUMERIC,
    _range REAL,
    _return REAL,
    _price_change REAL,
    _avg_price REAL,
    open_to_close_rt REAL,
    _price_dir TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(id)
    UNIQUE(company_id, date)
);