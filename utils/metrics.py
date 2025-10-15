import numpy as np
import pandas as pd
# import pandas_ta as ta

def price_metrics(df, period:str):

    df[period+'_range'] = df['high'] - df['low']
    df[period+'_return'] = df['adj_close'].pct_change() *100
    df[period+'_price_chge'] = (df['close'] - df['open'])/df['open'] * 100
    df[period+'_avg_price'] = (df['high'] + df['low'] + df['close']) / 3
    df[period+'_open_to_close_rt'] = df['open'] / df['close']
    df[period+'_price_dir'] = df.apply(lambda row: 'down' if row['close'] < row['open'] else 'up', axis=1)
    
    round_metrics = [period+'_return', period+'_price_chge', period+'_avg_price', period+'_open_to_close_rt']
    df[round_metrics] = df[round_metrics].round(3)
    
    return df


## TODO ##

def technical_analysis(df):
    pass