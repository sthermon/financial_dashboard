import requests
import pandas as pd
from collections import namedtuple
from rapidfuzz import process, fuzz, utils
from data_ingestion.fetch_data import company_check
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
    # print(sorted_matches)
        
    return sorted_matches


def process_results(symbol:str, matches):
    
    if not matches:
        return None, 0    
    
    best_match = process.extract_iter(symbol, choices=matches, processor=utils.default_process, scorer=fuzz.WRatio)
    
    first_el = list(best_match[0])
    # next((v for v in matches if v in [key] == best_match), None)
    print(first_el)
    
    
promtp = input("Enter company ticker:  ")
pull = get_company_info(promtp)
test = process_results(promtp, pull)


# [('Match',[symbol, name, score])]