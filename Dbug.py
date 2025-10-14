
import sys
import requests
from collections import namedtuple
from rapidfuzz import process


# def get_company_data(symbol:str, URL, API='13ULB7TGS4UJYQFH'):
#     '''
#         Function that will pull company information in json format and will select main interest points
#         to select and store in database
#     '''
#     payload = {'symbol':symbol, 'function':'OVERVIEW'}
#     try:
#         response = requests.get(f'{URL}/', params=payload)
#         response.raise_for_status()
        
#     except requests.RequestException:
#         return None

#     try:
#         dossier = response.json()
#         key_info = ['Symbol', 'Name', 'Exchange', 'Sector', 'DividendPerShare', 'DividendYield', 'EPS', '52WeekHigh', '52WeekLow', '50DayMovingAverage', '200DayMovingAverage','FiscalYearEnd', 'LatestQuarter', 'DividendDate', 'ExDividendDate']
#         return {
#             key: dossier[key] for key in key_info if key in dossier
#         }
        
#     except (KeyError, TypeError, ValueError):
#         return None




#url = 'https://www.alphavantage.co/query?function=IVERVIEW&tickers=AAPL&topics=financial_markets&apikey=13ULB7TGS4UJYQFH'
url = 'https://www.alphavantage.co/query?&apikey=13ULB7TGS4UJYQFH'
#url = 'https://www.alphavantage.co/query?'
ticker = 'NVDA'


# 925F1XGY0PDX1AK0
URL_KEY = 'https://www.alphavantage.co/query?&apikey=13ULB7TGS4UJYQFH'

'https://www.exampleurl.com/query?function=OVERVIEW&symbol=AAPL&apikey=demo'


# def company_check(symbol:str):
#     '''Fuction that will query company information on url and will return a 
#         set if possible matches to be displayed on main app. 
#         Accepts a ticker text from the user interface
#     '''
#     parameters = {'function':'SYMBOL_SEARCH', 'keywords':symbol}
#     try:
#         response = requests.get(URL_KEY, params=parameters)
#         response.raise_for_status()
        
#     except requests.RequestException:
#         return None
    
#     try:
#         result = response.json()
#         return result
#         # return {
#         #     'name': result['name'],
#         #     'symbol': result['symbol'],
#         #     'match': result['matchScore']
#         # }
    
#     except (KeyError, TypeError, ValueError):
#         return 'Not found'

# query = company_check('Apple')

# results = []

# for fields in query:
    
# query.get('bestMatches', {}).get()

# rl = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=NVDA&apikey=13ULB7TGS4UJYQFH'



reslt = {'bestMatches': [{'1. symbol': 'IBM', '2. name': 'International Business Machines Corp', '3. type': 'Equity', '4. region': 'United States', '5. marketOpen': '09:30', '6. marketClose': '16:00', '7. timezone': 'UTC-04', '8. currency': 'USD', '9. matchScore': '1.0000'}, {'1. symbol': 'IBMN', '2. name': 'ISHARES IBONDS DEC 2025 TERM MUNIBOND ETF ', '3. type': 'ETF', '4. region': 'United States', '5. marketOpen': '09:30', '6. marketClose': '16:00', '7. timezone': 'UTC-04', '8. currency': 'USD', '9. matchScore': '0.8571'}, {'1. symbol': 'IBMO', '2. name': 'ISHARES IBONDS DEC 2026 TERM MUNI BOND ETF ', '3. type': 'ETF', '4. region': 'United States', '5. marketOpen': '09:30', '6. marketClose': '16:00', '7. timezone': 'UTC-04', '8. currency': 'USD', '9. matchScore': '0.8571'}, {'1. symbol': 'IBMP', '2. name': 'ISHARES IBONDS DEC 2027 TERM MUNI BOND ETF ', '3. type': 'ETF', '4. region': 'United States', '5. marketOpen': '09:30', '6. marketClose': '16:00', '7. timezone': 'UTC-04', '8. currency': 'USD', 
'9. matchScore': '0.8571'}, {'1. symbol': 'IBMQ', '2. name': 'ISHARES IBONDS DEC 2028 TERM MUNI BOND ETF ', '3. type': 'ETF', '4. region': 'United States', '5. marketOpen': '09:30', '6. marketClose': '16:00', '7. timezone': 'UTC-04', '8. currency': 'USD', '9. matchScore': '0.8571'}, {'1. symbol': 'IBMR', '2. name': 'ISHARES IBONDS DEC 2029 TERM MUNI BOND ETF ', '3. type': 'ETF', '4. region': 'United States', '5. marketOpen': '09:30', '6. marketClose': '16:00', '7. timezone': 'UTC-04', '8. currency': 'USD', '9. matchScore': '0.8571'}, {'1. symbol': 'IBM.FRK', '2. name': 'International Business Machines', '3. type': 'Equity', '4. region': 'Frankfurt', '5. marketOpen': '08:00', '6. marketClose': '20:00', '7. timezone': 'UTC+02', '8. currency': 'EUR', 
'9. matchScore': '0.7500'}, {'1. symbol': 'IBM.DEX', '2. name': 'International Business Machines', '3. type': 'Equity', '4. region': 'XETRA', '5. marketOpen': '08:00', '6. marketClose': '20:00', '7. timezone': 'UTC+02', '8. currency': 'EUR', '9. matchScore': '0.6667'}, {'1. symbol': 'IBM0.FRK', '2. name': 'IBM CDR', '3. type': 'Equity', '4. region': 'Frankfurt', '5. marketOpen': '08:00', '6. marketClose': '20:00', '7. timezone': 'UTC+02', '8. currency': 'EUR', '9. matchScore': '0.6667'}, {'1. symbol': 'IBMB34.SAO', '2. name': 'International Business Machines Corp', '3. type': 'Equity', '4. region': 'Brazil/Sao Paolo', '5. marketOpen': '10:00', '6. marketClose': '17:30', '7. timezone': 'UTC-03', '8. currency': 'BRL', '9. matchScore': '0.5000'}]}

# extract = reslt.get('bestMatches', {}).get('9. matchScore')
# print(len(reslt.get('bestMatches')))
# print(reslt.get('bestMatches')[0].get('9. matchScore'))


# SearchResults = namedtuple('SearchResult',['symbol', 'name', 'matchscore'])

# matches = reslt.get('bestMatches', [])
# resul_list = []
# for match in matches:
#     company_symbol = match['1. symbol']
#     company_name = match['2. name']
#     search_score = match['9. matchScore']
#     query = SearchResults(company_symbol, company_name, search_score)
#     resul_list.append(query)
#     # resul_list.sort()
    
def get_company_info(symbol:str, result):
    '''
        Function that receives the user entry and calls an API to receive the most relevant results
        extract the name, symbol and sort the score returning a list.
    '''
    
    inquiry = result
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
        # logger.error(f'Search failed: {e}')
        return 'Unable to complete'
        
    print(f'sorted matches are as follow: /n {sorted_matches}')
    print('*'*100)
    filtered = rank_results(symbol, sorted_matches)
    return filtered


def rank_results(symbol:str, matches, limit=4):
    
    ranked = process.extract(symbol, matches, limit=limit)    
    if not matches:
        return []
    print(ranked[2][0])
    return ranked
    
print(get_company_info('ibm', reslt))


# (('symbol'['name','score']), ('symbol'['name','score']))
# response = requests.get(rl)
# data = response.json()
# print(data)

# print(sample)

#{'Symbol': 'AAPL', 'Name': 'Apple Inc', 'Exchange': 'NASDAQ', 'Sector': 'TECHNOLOGY', 
# 'DividendPerShare': '1.01', 'DividendYield': '0.0039', 'EPS': '6.59', '52WeekHigh': '259.18', 
# '52WeekLow': '168.8', '50DayMovingAverage': '228.45', '200DayMovingAverage': '221.97', 
# 'FiscalYearEnd': 'September', 'LatestQuarter': '2025-06-30', 'DividendDate': '2025-08-14', 
# 'ExDividendDate': '2025-08-11'}


# {'Global Quote': 
# {'01. symbol': 'IBM', '02. open': '256.9500', '03. high': '257.2500', '04. low': '252.4250', 
# '05. price': '253.4400', '06. volume': '3400380', '07. latest trading day': '2025-09-12', 
# '08. previous close': '257.0100', '09. change': '-3.5700', '10. change percent': '-1.3891%'}
# }
