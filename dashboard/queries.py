import requests
import streamlit as st
import pandas as pd
from data_ingestion.fetch_data import company_info, daily_activity, quote_historic_data
from data_ingestion.load_data import load_company_data, retrieve_company_data, load_periodic_data, load_daily_data, retrieve_periodic_data
from data_ingestion.clean_data import clean_company_info, clean_stock
from utils.db_connection import logger

# Check for database information first, otherwise pull information from API
@st.cache_resource
def get_company_info(symbol:str):
    '''
        Function that receives the user entry and calls an API to receive the most relevant results
        extract the name, symbol and sort the score returning a list.
    '''
    #Function that will query company information from an usl and return a JSON
    try:
        local_inquiry = retrieve_company_data(symbol)
        if local_inquiry == None:
            quote = company_info(symbol)
            if quote == None:
                return 'Unable to complete API call'
            load_company_data(symbol, quote)
            company_quote = pd.DataFrame([quote])
            clean_quote = clean_company_info(company_quote)
            return clean_quote
        
        
        inquiry = pd.DataFrame([local_inquiry])
        clean_inquiry = clean_company_info(inquiry)
        return clean_inquiry
            
    except requests.RequestException as e:
        logger.error(f'Search failed: {e}')
        return 'Unable to complete'



def company_info_day(symbol:str):

    quote = daily_activity(symbol)
    if isinstance(quote, pd.DataFrame):
        data = pd.DataFrame.from_dict(quote)
        data = data.infer_objects().reset_index().rename(columns={'index':'Date'})
        success = load_daily_data(symbol, data)
        if success:
            print(f'Data added for {symbol}')
        return data
    else:
        print(f'Unable to open file: Filetype: {type(quote)}')



def submit_historic_inquiry(symbol:str, period='weekly'):
    
    try:
        local_batch = retrieve_periodic_data(symbol)
        if local_batch == None:
            df = quote_historic_data(symbol, period)
            if df == None:
                return 'Unable to complete API call'
            data = clean_stock(df, period)
            load_periodic_data(symbol, period, data)
            clean_data = pd.DataFrame(data)
            return clean_data
        
        inquiry = pd.DataFrame([local_batch])
        # Pending to see neat and clean company data
        return inquiry
    
    except requests.RequestException as e:
        logger.error(f'Search failed: {e}')
        return 'Unable to complete'