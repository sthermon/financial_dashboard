import sqlite3
import pandas as pd
import streamlit as st
import json
from data_ingestion.fetch_data import quote_historic_data
from data_ingestion.clean_data import clean_stock
from utils.db_connection import connect_db, logger


@st.cache_resource
def load_company_data(symbol:str, quote):
    
    try:
        with connect_db() as conn:
            conn.cursor()
            conn.execute(
                '''
                INSERT OR REPLACE INTO companies(
                name, symbol, sector, open, current_price, previous_close, volume, average_volume, 
                eps_current_year, week_52_high, week_52_low, payout_ratio, target_mean_price, 
                dividend_rate, market_sentiment
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                , (
            quote.get('name'),
            quote.get('symbol'),
            quote.get('sector'),
            float(quote.get('open')),
            float(quote.get('current_price')),
            float(quote.get('previous_close')),
            int(quote.get('volume')),
            int(quote.get('average_volume')),
            float(quote.get('eps_current_year')),
            float(quote.get('week_52_high')),
            float(quote.get('week_52_low')),
            float(quote.get('payout_ratio')),
            float(quote.get('target_mean_price')),
            quote.get('dividend_rate'),
            quote.get('market_sentiment'),
            )
        )
        conn.commit()
        print(f'Company information for {symbol} uploaded')
        return True
    except Exception as e:
        logger.error(f' Error inserting data for {symbol}: "{e}"')
        return False
    
    
   
@st.cache_resource
def load_daily_data(symbol:str, quote):
    
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            for _, row in quote.iterrows():
                cursor.execute(
                '''
                    INSERT OR REPLACE INTO financial_metrics(
                        global_id, date, symbol, open, high, low, close, volume, dividends, stock_splits
                    )
                    SELECT (SELECT id FROM companies where symbol=?),
                    (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    symbol.upper(),
                    row['Date'],
                    float(row.get('Open')),
                    float(row.get('High')),
                    float(row.get('Low')),
                    float(row.get('Close')),
                    int(row.get('Volume')),
                    row.get('Dividends'),
                    row.get('Stock Splits'),
                    )   
                )
        conn.commit()
        return True
    except Exception as e:
        logger.error(f' Error inserting data for {symbol}: {e}')
        return False


##TODO "table periodic_metrics has no column named _price_change"
@st.cache_resource
def load_periodic_data(symbol:str, period:str, data):
    # data = clean_stock(symbol, period)
    conn = connect_db()
    try:
        for _, row in data.iterrows():
            conn.execute(
                '''
                INSERT OR REPLACE INTO periodic_metrics
                (company_id, date, open, high, low, close, adjusted_close,volume, dividend_amt,
                _range, _return, _price_change, _avg_price, _open_to_close_ratio, _price_direction)
                SELECT (
                    (SELECT id FROM companies where symbol=?),
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                '''.format(period, period, period, period, period, period),
                (
                    # symbol.upper(),
                    row['date'],
                    row.get('open'),
                    row.get('high'),
                    row.get('low'),
                    row.get('close'),
                    row.get('adj_close'),
                    row.get('volume'),
                    row.get('dividend_amt'),
                    row.get(period+'_range'),
                    row.get(period+'_return'),
                    row.get(period+'_price_change'),
                    row.get(period+'_avg_price'),
                    row.get(period+'_open_to_close_rt'),
                    row.get(period+'_price_dir')
                )
            )
        conn.commit()
    except Exception as e:
        logger.error(f"Error inserting data for {symbol}: {e}")
        return False
    finally:
        conn.close()
        return True

@st.cache_resource
def retrieve_company_data(symbol:str):
    
    try:
        conn = connect_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM companies WHERE symbol = ?', (symbol,))
        result = cur.fetchone()
        if result:
            return dict(result)
        return None
    
    except Exception as e:
        logger.error(f' Error retrieving data for {symbol}: "{e}"')
        return None
    finally:
        conn.close()

##TODO Error retrieving data for MSFT: no such column: symbol
def retrieve_periodic_data(symbol:str):
    
    try:
        conn = connect_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM periodic_metrics WHERE symbol =?', (symbol,))
        result = cur.fetchmany()
        if result:
            return dict(result)
        return None
    
    except Exception as e:
        logger.error(f'Error retrieving data for {symbol}: {e}')
        return None
    finally:
        conn.close()
    
