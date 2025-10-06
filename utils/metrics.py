import numpy as np
import pandas_ta as ta
import pandas as pd

def price_metrics(df, period:str):

    df = pd.read_csv(df)
    df[period+'_range'] = df['High'] - df['Low']
    df[period+'_return'] = df['Adj_close'].pct_change() *100
    df[period+'_price_chge'] = (df['Close'] - df['Open'])/df['Open'] * 100
    df[period+'_avg_price'] = (df['High'] + df['Low'] + df['Close']) / 3
    df[period+'_open_to_close_rt'] = df['Open'] / df['Close']
    df[period+'_price_dir'] = df.apply(lambda row: 'down' if row['Close'] < row['Open'] else 'up', axis=1)
    
    round_metrics = [period+'_return', period+'_price_chge', period+'_avg_price', period+'_open_to_close_rt']
    df[round_metrics] = df[round_metrics].round(3)
    
    return df


## TODO ##

def technical_analysis(df):
    pass