
-- Companies Table

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY, 
    name TEXT NOT NULL, 
    symbol TEXT UNIQUE, 
    sector TEXT,
    exchange TEXT, 
    eps NUMERIC , 
    week_52_high NUMERIC, 
    week_52_low NUMERIC, 
    moving_average_50_day_ NUMERIC, 
    moving_average_200_day_ NUMERIC, 
    dividend_per_share NUMERIC, 
    dividend_yield REAL, 
    fiscal_year_end TEXT, 
    latest_quarter TEXT, 
    dividend_date TEXT, 
    last_dividend_date TEXT
);

-- Financial metrics table

CREATE TABLE IF NOT EXISTS financial_metrics (
    id INTEGER PRIMARY KEY,
    date DATE,
    open REAL,
    high REAL,
    low, REAL,
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
## TODO ## Update schema with dynamic table

CREATE TABLE IF NOT EXISTS pediodic_metrics (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    date DATE,
    open REAL,
    high REAL,
    low, REAL,
    close REAL,
    adjusted_close REAL,
    volume NUMERIC,
    dividend_amt NUMERIC,
    _range REAL,
    _return REAL,
    _price_change REAL,
    _avg_price REAL,
    _open_to_close_ratio REAL,
    _price_direction TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(id)
    UNIQUE(company_id, date)
);