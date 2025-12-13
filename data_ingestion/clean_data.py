import pandas as pd
from io import BytesIO
from utils.metrics import price_metrics
from utils.db_connection import logger


def clean_stock(dataframe, frequency:str):
    '''
        Function that will accept and call other functions to clean 
        rename and add aggregated metrics returning the clean Dataframe
    '''
    df = dataframe
    if isinstance(df, bytes):
        data = pd.read_csv(BytesIO(df))
        company_data = data.copy()
        
    elif isinstance(df, pd.DataFrame):
        company_data = data.copy()
        
    else:
        raise ValueError(f'Unsupported input type: Filetype: {type(df)} ')
    
    company_data = data.copy()
    company_data = company_data.infer_objects()
    company_data.sort_index(inplace=True)
    clean_data = company_data.dropna()
    new_data = reshape_data(clean_data, frequency)
    return new_data


def reshape_data(df, period:str):
    '''
        Function that renames colums from a Dataframe and merges calculated metrics
    '''
    n_columns = {
        'timestamp': 'date', 
        'open': 'open', 
        'high': 'high', 
        'low': 'low', 
        'close': 'close', 
        'adjusted close': 'adj_close', 
        'volume': 'volume', 
        'dividend amount': 'dividend_amt'
    }
    data = df.rename(columns = n_columns)
    update_data = price_metrics(data, period.lower())
    
    dataf = pd.DataFrame(update_data)
    return dataf


def clean_company_info(df):
    '''
        Function that renames column names for cleanliness and company displaying.
    '''
    
    column_names = ['Name', 'Symbol', 'Sector', 'Current Price', 'Open', 'Previous Close' , 'Volume', 'Market Sentiment']
    data = df.copy()
    data = data[['name', 'symbol', 'sector', 'current_price', 'open', 'previous_close', 'volume', 'market_sentiment']]
    data.columns = column_names
    return data

