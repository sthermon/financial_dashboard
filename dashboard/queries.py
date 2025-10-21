import requests
from collections import namedtuple
from rapidfuzz import process, fuzz
from data_ingestion.fetch_data import company_check, pull_company_data
from data_ingestion.load_data import load_company_data, load_daily_data
from utils.db_connection import logger


def get_company_info(symbol:str):
    '''
        Function that receives the user entry and calls an API to receive the most relevant results
        extract the name, symbol and sort the score returning a list.
    '''
    
    inquiry = company_check(symbol)
    
    Match = namedtuple('Match', ['symbol', 'name', 'score'])
    try:
        bestmatches = inquiry.get('bestMatches', [])
        matches = [
            Match(
            match['1. symbol'],
            match['2. name'],
            float(match['9. matchScore'])
        )
        for match in bestmatches
        ]
        sorted_matches = sorted(matches, key=lambda x: x.score, reverse=True)
            
    except requests.RequestException as e:
        logger.error(f'Search failed: {e}')
        return 'Unable to complete'
        
    return sorted_matches


def process_results(symbol:str, matches, top=5):
    
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
    
    dossier = pull_company_data(symbol)
    load_company_data(symbol)
    load_daily_data(symbol)
    return dossier