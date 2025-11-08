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
            int(quote.get('volume', 0)),
            int(quote.get('average_volume', 0)),
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
            global_id = cursor.execute(
                'SELECT id FROM companies WHERE symbol=?',
                (symbol.upper(),)
            ).fetchone()[0]
            
            for _, row in quote.iterrows():
                date_value = row['Date'].to_pydatetime().date()
                cursor.execute(
                    '''
                    INSERT OR REPLACE INTO financial_metrics
                    (global_id, date, symbol, open, high, low, close, volume, dividends, stock_splits)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                (
                    global_id,
                    date_value,
                    symbol.upper(),
                    float(row.get('Open')),
                    float(row.get('High')),
                    float(row.get('Low')),
                    float(row.get('Close')),
                    row.get('Volume', 0),
                    row.get('Dividends', 0),
                    row.get('Stock Splits'),
                    )   
                )
        conn.commit()
        return True
    except Exception as e:
        logger.error(f' Error inserting data for {symbol}: {e}')
        return False


@st.cache_resource
def load_periodic_data(symbol:str, period:str, data):
    # data = clean_stock(symbol, period)
    conn = connect_db()
    try:
        company_id = conn.execute(
            'SELECT id FROM companies WHERE symbol=?',
            (symbol.upper(),)
        ).fetchone()[0]
        
        for _, row in data.iterrows():
            conn.execute(
                '''
                INSERT OR REPLACE INTO periodic_metrics
                (company_id, date, open, high, low, close, adjusted_close, volume, dividend_amt,
                _range, _return, _price_change, _avg_price, open_to_close_rt, _price_dir)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    company_id,
                    row['date'],
                    row.get('open'),
                    row.get('high'),
                    row.get('low'),
                    row.get('close'),
                    row.get('adj_close'),
                    row.get('volume'),
                    row.get('dividend_amt'),
                    row.get(f'{period}_range'),
                    row.get(f'{period}_return'),
                    row.get(f'{period}_price_change'),
                    row.get(f'{period}_avg_price'),
                    row.get(f'{period}_open_to_close_rt'),
                    row.get(f'{period}_price_dir')
                )
            )
        conn.commit()
    except Exception as e:
        logger.error(f'Error inserting periodic data for {symbol}: {e}')
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



def retrieve_periodic_data(symbol:str):
    
    try:
        conn = connect_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('''
                SELECT periodic_metrics.*
                FROM periodic_metrics
                INNER JOIN companies ON periodic_metrics.company_id = companies.id
                WHERE companies.symbol = ?
                ''', (symbol.upper(),))
        result = cur.fetchall()
        if result:
            return [dict(row) for row in result]
        return None
    
    except Exception as e:
        logger.error(f'Error retrieving periodic data for {symbol}: {e}')
        return None
    finally:
        conn.close()
    
