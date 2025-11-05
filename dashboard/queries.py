import requests
import streamlit as st
import pandas as pd
from data_ingestion.fetch_data import company_info
from data_ingestion.load_data import load_company_data, retrieve_company_data, periodic_data
# from data_ingestion.clean_data import
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
            company_quote = pd.DataFrame.from_dict(quote, orient='columns')
            return company_quote
        
        inquiry = pd.DataFrame([local_inquiry])
        return inquiry
            
    except requests.RequestException as e:
        logger.error(f'Search failed: {e}')
        return 'Unable to complete'


def submit_selection(symbol:str):
    pass
    # dossier = pull_company_data(symbol)
    dossier = periodic_data(symbol, period='weekly')
    if load_company_data(symbol, dossier):
       
        print('Company updated to database')
    return dossier