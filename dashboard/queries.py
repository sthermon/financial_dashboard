import requests
import streamlit as st
from collections import namedtuple
from rapidfuzz import process, fuzz
from data_ingestion.fetch_data import quote_historic_data, company_info
from data_ingestion.load_data import load_company_data, load_daily_data, retrieve_company_data, periodic_data
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
            inquiry = company_info(symbol)
            load_company_data(symbol, inquiry)
            if inquiry == None:
                return 'Unable to complete API call'
        return inquiry
            
    except requests.RequestException as e:
        logger.error(f'Search failed: {e}')
        return 'Unable to complete'
        


def process_results(symbol:str, matches, top=5):
    '''
        Function designed to process word matches and return the best scored matches in order
    '''
    if not matches:
        return []  

    # To N of matches above with top score
    top_matches = process.extract(
        symbol,
        choices=matches,
        scorer=fuzz.WRatio,
        limit=top,    
    )

    # List of tuples (match, score) processing therapidfuzz result
    return [(match, score) for match, score, _ in top_matches]
    
    
def submit_selection(symbol:str):
    pass
    # dossier = pull_company_data(symbol)
    periodic_data(symbol, period='weekly')
    if load_company_data(symbol, dossier):
       
        print('Company updated to database')
    return dossier