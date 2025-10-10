from collections import namedtuple
import requests
import pandas as pd
from data_ingestion.fetch_data import company_check
from utils.db_connection import logger


def submit_inquiry(symbol:str):
    '''
        Function that receives the user entry and calls an API to receive the most relevant results
        extract the name, symbol and sort the score returning a list.
    '''
    
    inquiry = company_check(symbol)
    
    Match = namedtuple('Match'['symbol', 'name', 'score'])
    try:
        bestmatches = inquiry.get('bestMatches', [])
        matches = [
            Match(
            match['2. name'],
            match['1. symbol'],
            float(match['9. matchScore'])
        )
        for match in bestmatches
        ]
        sorted_matches = sorted(matches, lambda x: x.score, reverse=True)
            
            
    except requests.RequestException as e:
        logger.error(f'Search failed: {e}')
        return 'Unable to complete'
        
    return sorted_matches



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
