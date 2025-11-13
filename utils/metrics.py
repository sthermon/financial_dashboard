import numpy as np
import pandas as pd


def price_metrics(df, period: str):
    '''
    Function that calculates and add aggregated metrics based on a frequency and range of values form the company
    returns a formatted Dataframe
    '''
    df['range'] = df['high'] - df['low']
    df['return'] = df['adj_close'].pct_change() * 100
    df['price_change'] = (df['close'] - df['open'])/df['open'] * 100
    df['avg_price'] = (df['high'] + df['low'] + df['close']) / 3
    df['open_to_close_rt'] = df['open'] / df['close']
    df['price_dir'] = df.apply(lambda row: 'down' if row['close'] < row['open'] else 'up', axis=1)
    df['frequency'] = period
    round_metrics = ['return', 'price_change', 'avg_price', 'open_to_close_rt']
    df[round_metrics] = df[round_metrics].round(3)
        
    return df


    