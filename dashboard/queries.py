from collections import namedtuple
import requests
import pandas as pd
from rapidfuzz import process, fuzz
from data_ingestion import company_check
from utils import logger


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


def process_results(symbol:str, matches:list, key='name'):
    
    if not matches:
        return None, 0    
    
    best_match, score, _ = process.extractOne(symbol, matches, scorer=fuzz.WRatio)
    
    matched_search = next((v for v in matches if v in [key] == best_match), None)
    
    return matched_search, score

