import requests
import pandas as pd
import streamlit as st
import numpy as np
from data_ingestion.fetch_data import company_check
from utils.db_connection import logger

## TODO ##
'''Update function to pull information from the fetch file'''

query = company_check(symbol)
    


'''Code example'''
import pandas as pd
from utils.db_connection import get_connection

def company_exists(symbol: str) -> bool:
    conn = get_connection()
    query = "SELECT 1 FROM companies WHERE ticker=? LIMIT 1"
    result = conn.execute(query, (symbol,)).fetchone()
    conn.close()
    return result is not None

def get_company_metrics(ticker: str):
    conn = get_connection()
    query = """
        SELECT date, revenue, profit, eps,
               profit_margin, revenue_growth, eps_growth, stock_price
        FROM financial_metrics
        JOIN companies ON financial_metrics.company_id = companies.id
        WHERE companies.ticker=?
        ORDER BY date
    """
    df = pd.read_sql(query, conn, params=(ticker,))
    conn.close()
    return df
