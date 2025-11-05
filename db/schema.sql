
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    symbol TEXT,
    open REAL,
    high REAL,
    low REAL,
    price REAL,
    previous_close REAL,
    volume NUMERIC,
    change REAL,
    change_percentage REAL,
    global_id INTEGER NOT NULL,
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
    _range REAL,
    _return REAL,
    _price_chge REAL,
    _avg_price REAL,
    open_to_close_rt REAL,
    price_dir TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(id)
    UNIQUE(company_id, date)
);