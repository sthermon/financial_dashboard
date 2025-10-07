import pandas as pd
from fetch_data import quote_historic_data
from utils.metrics import price_metrics
from utils.db_connection import logger


def clean_stock(symbol, period:str):
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


def reshape_data(df, period):
    '''
        Function that renames colums from a Dataframe and merges calculated metrics
    '''
    n_columns = {'date': 'date', 'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close', 
                 'adj_close': 'adj_close', 'volume': 'volume', 'dividend_amt': 'dividend_amt'}
    data = df.rename(columns = n_columns)
    update_data = price_metrics(data, period)
    
    return pd.DataFrame(update_data)
