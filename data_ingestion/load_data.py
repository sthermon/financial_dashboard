import pandas as pd
import sqlite3
from data_ingestion import pull_company_data, quote_data, quote_historic_data
from data_ingestion import clean_stock
from utils import connect_db, logger


def load_company_data(symbol:str):
    
    quote = pull_company_data(symbol)
    conn = connect_db()
    try:
        conn.execute(
            '''
                INSERT OR IGNORE INTO companies(
                name, symbol, sector, exchange, eps, week_52_high, week_52_low, moving_average_50_day_,
                moving_average_200_day_, dividend_per_share, dividend_yield, fiscal_year_end, latest_quarter, 
                dividend_date, last_dividend_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    
            ''', (
            quote.get('Name'),
            quote.get('Symbol'),
            quote.get('Sector'),
            quote.get('Exchange'),
            quote.get('EPS'),
            quote.get('52WeekHigh'),
            quote.get('52WeekLow'),
            quote.get('50DayMovingAverage'),
            quote.get('200DayMovingAverage'),
            quote.get('DividendPerShare'),
            quote.get('DividendYield'),
            quote.get('FiscalYearEnd'),
            quote.get('LatestQuarter'),
            quote.get('DividendDate'),
            quote.get('ExDividendDate')
            )
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
    finally:
        conn.close()
   
    
    
def load_daily_data(symbol:str):
    
    data = quote_data(symbol)
    conn = connect_db()
    try:
        conn.execute(
            '''
                INSERT OR IGNORE INTO financial_metrics(
                    global_id, date, symbol, open, high, low, price, previous_close, volume, change, change_percentage
                )
                SELECT (SELECT id FROM companies where symbol=?),
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                data.get('Global Quote', {}).get('07. latest trading day'),
                data.get('Global Quote', {}).get('01. symbol'),
                data.get('Global Quote', {}).get('02. open'),
                data.get('Global Quote', {}).get('03. high'),
                data.get('Global Quote', {}).get('04. low'),
                data.get('Global Quote', {}).get('05. price'),
                data.get('Global Quote', {}).get('08. previous close'),
                data.get('Global Quote', {}).get('06. volume'),
                data.get('Global Quote', {}).get('09. change'),
                data.get('Global Quote', {}).get('10. change percent'),
            )
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
    finally:
        conn.close()



def periodic_data(symbol:str, period:str):
    pass
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


