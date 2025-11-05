import pandas as pd
from io import BytesIO
from data_ingestion.fetch_data import quote_historic_data, daily_activity
# from data_ingestion.load_data import load_daily_data
from utils.metrics import price_metrics
from utils.db_connection import logger


def clean_stock(symbol:str, period='weekly'):
    '''
        Function that will accept and call other functions to clean 
        rename and add aggregated metrics returning the clean Dataframe
    '''
    
    df = quote_historic_data(symbol, period)
    if isinstance(df, bytes):
        data = pd.read_csv(BytesIO(df))
        data = df.copy()
        data = data.infer_objects()
        data.sort_index(inplace=True)
        null_values = data.isna().sum()
        clean_data = data.dropna()
        logger.info(f'A total of {null_values.sum()} were dropped')
        new_data = reshape_data(clean_data, period)
        return new_data
    else:
        print(f'Unable to access file: Filetype: {type(df)} ')


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
    
    quote = daily_activity(symbol)
    if isinstance(quote, pd.DataFrame):
        data = pd.DataFrame.from_dict(quote)
        data = data.infer_objects().reset_index().rename(columns={'index':'Date'})
        # success = load_daily_data(symbol, data)
        # if success:
        #     print(f'Data added for {symbol}')
        return data #if success else f'Failed to load data for {symbol}'
    else:
        print(f'Unable to open file: Filetype: {type(quote)}')

