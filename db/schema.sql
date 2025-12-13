
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
    average_volume REAL,
    eps_current_year REAL,
    P_to_E_ratio REAL,
    week_52_high REAL,
    week_52_low REAL,
    payout_ratio REAL,
    target_mean_price REAL,
    all_time_high REAL,
    all_time_low REAL,
    market_cap REAL,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    date DATE,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adjusted_close REAL,
    volume NUMERIC,
    dividend_amt NUMERIC,
    range REAL,
    return REAL,
    price_change REAL,
    avg_price REAL,
    open_to_close_rt REAL,
    price_dir TEXT,
    frequency TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(id)
    UNIQUE(company_id, date, frequency)
);