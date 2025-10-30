import sqlite3
import pandas as pd
import streamlit as st
import json
from data_ingestion.fetch_data import quote_historic_data, quote_data
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
                name, symbol, sector, open, previous_close, volume, eps_current_year, fifty_two_week_high,
                fifty_two_week_low, ex_dividend_date, payout_ratio, fiscal_year_end, most_recent_quarter, 
                annual_dividend_rate, last_dividend_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    
                '''
            , (
            quote.get('displayName'),
            quote.get('symbol'),
            quote.get('sector'),
            quote.get('open'),
            quote.get('previousClose'),
            quote.get('volume'),
            quote.get('epsCurrentYear'),
            quote.get('fiftyTwoWeekHigh'),
            quote.get('fiftyTwoWeekLow'),
            quote.get('exDividendDate'),
            quote.get('payoutRatio'),
            quote.get('lastFiscalYearEnd'),
            quote.get('mostRecentQuarter'),
            quote.get('trailingAnnualDividendRate'),
            quote.get('exDividendDate'),
            )
        )
        conn.commit()
        print(f'Company information for {symbol} uploaded')
        return True
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        return False
   
    
@st.cache_resource
def load_daily_data(symbol:str, quote):
    
    try:
        with connect_db() as conn:
            conn.cursor()
            conn.execute(
            '''
                INSERT OR IGNORE INTO financial_metrics(
                    global_id, date, symbol, open, high, low, price, previous_close, volume, change, change_percentage
                )
                SELECT (SELECT id FROM companies where symbol=?),
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol.upper(),
                quote.get('Global Quote', {}).get('07. latest trading day'),
                quote.get('Global Quote', {}).get('01. symbol'),
                quote.get('Global Quote', {}).get('02. open'),
                quote.get('Global Quote', {}).get('03. high'),
                quote.get('Global Quote', {}).get('04. low'),
                quote.get('Global Quote', {}).get('05. price'),
                quote.get('Global Quote', {}).get('08. previous close'),
                quote.get('Global Quote', {}).get('06. volume'),
                quote.get('Global Quote', {}).get('09. change'),
                quote.get('Global Quote', {}).get('10. change percent'),
            )
        )
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        return False


@st.cache_resource
def periodic_data(symbol:str, period:str):
    data = clean_stock(symbol, period)
    conn = connect_db()
    try:
        for _, row in data.iterrows():
            conn.execute(
                '''
                INSERT OR REPLACE INTO periodic_metrics
                (company_id, date, open, high, low, close, adjusted_close,volume, dividend_amt
                _range, _return, _price_change, _avg_price, _open_to_close_ratio, _price_direction)
                SELECT (
                    (SELECT id FROM companies where symbol=?),
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                '''.format(period, period, period, period, period, period),
                (
                    symbol,
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
                    row.get(period+'_price_chge'),
                    row.get(period+'_avg_price'),
                    row.get(period+'_open_to_close_rt'),
                    row.get(period+'_price_dir')
                )
            )
        conn.commit()
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
    finally:
        conn.close()


#TODO UPDATE NAMES
def retrieve_company_data(symbol:str):
    
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM companies WHERE symbol = ?', (symbol,))
        result = cur.fetchall()
        if result:
            {
            'Name':result[0],
            'Symbol':result[1],
            'Sector':result[2],
            'Exchange':result[3],
            'EPS':result[4],
            '52WeekHigh':result[5],
            '52WeekLow':result[6],
            '50DayMovingAverage':result[7],
            '200DayMovingAverage':result[8],
            'DividendPerShare':result[9],
            'DividendYield':result[10],
            'FiscalYearEnd':result[11],
            'LatestQuarter':result[12],
            'DividendDate':result[13],
            'ExDividendDate':result[14]
            }
            return result #result #{'name': result[0], 'symbol': result[1]}
        return None
        
    except Exception as e:
        logger.error(f'Error retrieving data for {symbol}: {e}')
        return None
    finally:
        conn.close()


def retrieve_periodic_data(symbol:str):
    
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM periodic_metrics WHERE symbol =?', (symbol,))
        result = cur.fetchmany()
        if result:
            df = pd.DataFrame('periodic_metrics', result)
            return df
        return None
    
    except Exception as e:
        logger.error(f'Error retrieving data for {symbol}: {e}')
        return None
    finally:
        conn.close()
    
