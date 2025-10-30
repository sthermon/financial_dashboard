import pandas as pd
from data_ingestion.fetch_data import quote_historic_data, quote_data
from utils.metrics import price_metrics
from utils.db_connection import logger


def clean_stock(symbol:str, period:str):
    '''
        Function that will accept and call other functions to clean 
        rename and add aggregated metrics returning the clean Dataframe
    '''
    
    df = quote_historic_data(symbol, period)
    if isinstance(df, str):
        data = pd.read_csv(df, index_col=0)
    else:
        data = df.copy()
    data = data.infer_objects()
    data.sort_index(inplace=True)
    null_values = data.isna().sum()
    clean_data = data.dropna()
    logger.info(f'A total of {null_values.sum()} were dropped')
    new_data = reshape_data(clean_data, period)
    return new_data


def reshape_data(df, period:str):
    '''
        Function that renames colums from a Dataframe and merges calculated metrics
    '''
    n_columns = {'timestamp': 'date', 'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close', 
                 'adjusted close': 'adj_close', 'volume': 'volume', 'dividend amount': 'dividend_amt'}
    data = df.rename(columns = n_columns)
    update_data = price_metrics(data, period)
    
    return pd.DataFrame(update_data)

def daily_data_clean(symbol:str):
    
    quote = quote_data(symbol)
    data = pd.DataFrame.from_dict(quote, orient='index')
    columns = ['07. latest trading day', '01. symbol', '02. open','03. high','04. low','05. price','08. previous close','06. volume','09. change','10. change percent']
    column_names = ['last_trading_day', 'symbol', 'open', 'high', 'low', 'price', 'last_close', 'volume', 'change', 'change_pct']
    data_select = data.copy()
    new_selec = data_select[columns]
    new_selec.columns = column_names
    return new_selec

