import requests
import pandas as pd
import yfinance as yf
import streamlit as st
from collections import namedtuple
from utils import logger


API_KEY = st.secrets['api']['key']
API_URL = st.secrets['api']['url']


def quote_data(symbol:str) -> tuple:
    '''
        Function that receives a user search, process and returns 5 possible matches
        in a list of tuples
    '''
    search_results = yf.Search(symbol, max_results=5, news_count=0) 
    query = search_results.all
    Stocks = namedtuple('Stocks', ['symbol', 'longname', 'typeDisp'])
    try:
        companies = query.get('quotes', [])
        results = [
            Stocks(
            company['symbol'],
            company['longname'],
            company['typeDisp']
        )
        for company in companies
        ]
    except requests.RequestException as e:
        logger.error(f'Search failed: {e}')
        return 'Unable to complete'
        
    return results

@st.cache_data
def company_info(symbol:str):
    
    company = yf.Ticker(symbol)
    info = company.info
    summary = {
        'name':info['displayName'],
        'symbol':info['symbol'],
        'sector':info['sector'],
        'open':info['open'],
        'current_price':info['currentPrice'],
        'previous_close':info['previousClose'],
        'volume':info['volume'],
        'averageVolume':info['averageVolume'],
        'eps_current_year':info['epsCurrentYear'],
        'week_52_high':info['fiftyTwoWeekHigh'],
        'week_52_low':info['fiftyTwoWeekLow'],
        'payout_ratio':info['payoutRatio'],
        'target_mean_price':info['targetMeanPrice'],
        'dividend_rate':info['trailingAnnualDividendRate'],
        'market_sentiment':info['recommendationKey']
    }
    return summary
    
    
@st.cache_data
def daily_activity(symbol:str):
    
    try:
        ticker = yf.Ticker(symbol)
        ticker_day = ticker.history(period='1d')
        
    except requests.RequestException as e:
        logger.error(f'Search failed: {e}')
        return f'Unable to complete call for {symbol}: "{e}"'
    
    return ticker_day


@st.cache_data(show_spinner=False)
def quote_historic_data(symbol:str, period:str):
    
    series_list = ['TIME_SERIES_MONTHLY_ADJUSTED', 'TIME_SERIES_WEEKLY_ADJUSTED']
    frequency = series_list[0] if period == 'monthly' else series_list[1] if period == 'weekly' else None
    
    parameters = {'symbol':symbol, 'function':frequency, 'datatype':'csv', 'apikey':API_KEY}
    try:
        response = requests.get(f'{API_URL}/', params=parameters)
        response.raise_for_status()
        
    except requests.RequestException as e:
        logger.error(f'API request failed: {e}')
        return 'Unable to complete or not found'
    
    historic_data = response.content
    return historic_data
    
    