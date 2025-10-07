import streamlit as st
import requests
from utils.db_connection import logger


API_KEY = st.secrets['api']['key']
API_URL = st.secrets['api']['url']


def get_company_data(symbol:str):
    '''
        Function that will pull company information in json format and will select main interest points
        to select and store in database
    '''
    parameters = {'symbol':symbol, 'function':'OVERVIEW', 'apikey':API_KEY}
    try:
        response = requests.get(f'{API_URL}/',  params=parameters)
        response.raise_for_status()
        
    except requests.RequestException as e:
        logger.error(f'API request failed: {e}')
        return None

    try:
        dossier = response.json()
        key_info = ['Symbol', 'Name', 'Exchange', 'Sector', 'DividendPerShare', 'DividendYield', 'EPS', '52WeekHigh', '52WeekLow', '50DayMovingAverage', '200DayMovingAverage','FiscalYearEnd', 'LatestQuarter', 'DividendDate', 'ExDividendDate']
        return {
            key: dossier[key] for key in key_info if key in dossier
        }
        
    except (KeyError, TypeError, ValueError):
        return None


def quote_data(symbol:str):
    '''
        Function that retrieves the most recent information from a company and returns a csv file
    '''
    parameters = {'function':'GLOBAL_QUOTE', 'symbol':symbol, 'datatype':'json', 'apikey':API_KEY}
    
    try:
        response = requests.get(f'{API_URL}/', params={parameters})
        response.raise_for_status()
        
    except requests.RequestException as e:
        logger.error(f'API request failed: {e}')
        return None
    
    return response


def quote_historic_data(symbol:str, period:str):
    
    series_list = ['TIME_SERIES_MONTHLY_ADJUSTED', 'TIME_SERIES_WEEKLY_ADJUSTED']
    frequency = series_list[0] if period == 'monthly' else series_list[1] if period == 'weekly' else None
    
    parameters = {'symbol':symbol, 'function':frequency, 'datatype':'csv', 'apikey':API_KEY}
    try:
        response = requests.get(f'{API_URL}/', params=parameters)
        response.raise_for_status()
        
    except requests.RequestException as e:
        logger.error(f'API request failed: {e}')
        return None
    
    return response
    
    
##TODO##  Complete the search box button  
    
def company_check(symbol:str):
    '''Fuction that will query company information on url and will return a 
        set if possible matches to be displayed on main app. 
        Accepts a ticker text from the user interface
    '''
    parameters = {'function':'SYMBOL_SEARCH', 'keywords':symbol}
    headers={'Authorization': f'Bearer {API_KEY}'}
    try:
        response = requests.get(f'{API_URL}/', params=parameters, headers=headers)
        response.raise_for_status()
        
    except requests.RequestException:
        return None
    
    try:
        result = response.json()
        return {
            'name': result['name'],
            'symbol': result['symbol'],
            'match': result['matchScore']
        }
    
    except (KeyError, TypeError, ValueError):
        return 'Not found'
