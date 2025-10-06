
import sys
import requests


def get_company_data(symbol:str, URL, API='13ULB7TGS4UJYQFH'):
    '''
        Function that will pull company information in json format and will select main interest points
        to select and store in database
    '''
    payload = {'symbol':symbol, 'function':'OVERVIEW'}
    try:
        response = requests.get(f'{URL}/', params=payload)
        response.raise_for_status()
        
    except requests.RequestException:
        return None

    try:
        dossier = response.json()
        key_info = ['Symbol', 'Name', 'Exchange', 'Sector', 'DividendPerShare', 'DividendYield', 'EPS', '52WeekHigh', '52WeekLow', '50DayMovingAverage', '200DayMovingAverage','FiscalYearEnd', 'LatestQuarter', 'DividendDate', 'ExDividendDate']
        return {
            key: dossier[key] for key in key_info if key in dossier
        }
        
    except (KeyError, TypeError, ValueError):
        return None
    
    df[frequency+'_range'] = df['High'] - df['Low']
    df[frequency+'_return'] = df['Adj_close'].pct_change() *100
    df[frequency+'_price_change'] = (df['Close'] - df['Open'])/df['Open'] * 100
    df[frequency+'_avg_price'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['Open_to_close_ratio'] = df['Open'] / df['Close']
    df['Price_direction'] = df.apply(lambda row: 'down' if row['Close'] < row['Open'] else 'up', axis=1)

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
#url = 'https://www.alphavantage.co/query?function=IVERVIEW&tickers=AAPL&topics=financial_markets&apikey=13ULB7TGS4UJYQFH'
url = 'https://www.alphavantage.co/query?&apikey=13ULB7TGS4UJYQFH'
#url = 'https://www.alphavantage.co/query?'
ticker = 'NVDA'

sample = get_company_data(ticker, url)


def return_frq(period:str):
    
    time_list = ['TIME_SERIES_MONTHLY_ADJUSTED', 'TIME_SERIES_WEEKLY_ADJUSTED']
    frequency = time_list[0] if period == 'monthly' else time_list[1]
    
    # if period == 'monthly':
    #     'TIME_SERIES_MONTHLY_ADJUSTED'
    # elif period == 'weekly':
    #     'TIME_SERIES_WEEKLY_ADJUSTED'
    return frequency
    
    
print(return_frq('weekly'))    




'https://www.exampleurl.com/query?function=OVERVIEW&symbol=AAPL&apikey=demo'

# print(sample)


#{'Symbol': 'AAPL', 'Name': 'Apple Inc', 'Exchange': 'NASDAQ', 'Sector': 'TECHNOLOGY', 
# 'DividendPerShare': '1.01', 'DividendYield': '0.0039', 'EPS': '6.59', '52WeekHigh': '259.18', 
# '52WeekLow': '168.8', '50DayMovingAverage': '228.45', '200DayMovingAverage': '221.97', 
# 'FiscalYearEnd': 'September', 'LatestQuarter': '2025-06-30', 'DividendDate': '2025-08-14', 
# 'ExDividendDate': '2025-08-11'}


def load_financial_data(df, ticker):
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO companies (ticker, name) VALUES (?, ?)", (ticker, ticker))

    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO financial_metrics
            (company_id, date, revenue, profit, profit_margin, revenue_growth)
            VALUES (
                (SELECT id FROM companies WHERE ticker=?),
                ?, ?, ?, ?, ?
            )
        """, (
            ticker,
            row["date"],
            row["revenue"],
            row["profit"],
            row["profit_margin"],
            row["revenue_growth"]
        ))

    conn.commit()
    conn.close()




# {'Global Quote': 
# {'01. symbol': 'IBM', '02. open': '256.9500', '03. high': '257.2500', '04. low': '252.4250', 
# '05. price': '253.4400', '06. volume': '3400380', '07. latest trading day': '2025-09-12', 
# '08. previous close': '257.0100', '09. change': '-3.5700', '10. change percent': '-1.3891%'}
# }
