import requests
import yfinance as yf
import streamlit as st
from collections import namedtuple
from utils import logger


API_KEY = st.secrets['api']['key']
API_URL = st.secrets['api']['url']


@st.cache_data
def company_info(symbol:str):
    
    company = yf.Ticker(symbol)
    info = company.info
    ticker = {
        info['displayName'],
        info['symbol'],
        info['sector'],
        info['open'],
        info['previousClose'],
        info['volume'],
        info['epsCurrentYear'],
        info['fiftyTwoWeekHigh'],
        info['fiftyTwoWeekLow'],
        info['exDividendDate'],
        info['payoutRatio'],
        info['lastFiscalYearEnd'],
        info['mostRecentQuarter'],
        info['trailingAnnualDividendRate'],
        info['exDividendDate']
    }
        
    return ticker

def quote_data(symbol:str) -> tuple:
    '''
        Function that receives a user search, process and returns 5 possible matches
        in a list of tuples
    '''
    search_results = yf.Search(symbol, max_results=5, news_count=0) # Run tests for search functionality
    query = search_results.all
    Stocks = namedtuple('Match', ['symbol', 'shortname', 'typeDisp'])
    
    try:
        companies = query.get('quotes', [])
        results = [
            Stocks(
            company['symbol'],
            company['shortname'],
            company['typeDisp']
        )
        for company in companies
        ]
    except requests.RequestException as e:
        logger.error(f'Search failed: {e}')
        return 'Unable to complete'
        
    return results
    

@st.cache_data(show_spinner=False)
def quote_historic_data(symbol:str, period:str):
    
    series_list = ['TIME_SERIES_MONTHLY_ADJUSTED', 'TIME_SERIES_WEEKLY_ADJUSTED']
    frequency = series_list[0] if period == 'monthly' else series_list[1] if period == 'weekly' else None
    
    parameters = {'symbol':symbol, 'function':frequency, 'datatype':'json', 'apikey':API_KEY}
    try:
        response = requests.get(f'{API_URL}/', params=parameters)
        response.raise_for_status()
        
    except requests.RequestException as e:
        logger.error(f'API request failed: {e}')
        return 'Unable to complete or not found'
    
    historic_data = response.csv
    return historic_data
    
    