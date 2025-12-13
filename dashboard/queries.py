import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from data_ingestion.fetch_data import company_info, daily_activity, quote_historic_data, refresh_company_data
from data_ingestion.load_data import load_company_data, retrieve_company_data, load_periodic_data, load_daily_data, retrieve_periodic_data
from data_ingestion.clean_data import clean_company_info, clean_stock
from utils.db_connection import logger, connect_db


@st.cache_resource
def get_company_info(symbol:str):
    '''
        Function that receives the user entry and calls an API to receive the most relevant results
        extract the name, symbol and sort the score returning a list.
    '''
    try:
        local_inquiry = retrieve_company_data(symbol)
        if local_inquiry == None:
            quote = company_info(symbol)
            if quote == None:
                return 'Unable to complete API call'
            load_company_data(symbol, quote)
            company_quote = pd.DataFrame([quote])
            clean_quote = clean_company_info(company_quote)
            return clean_quote
        
        inquiry = pd.DataFrame([local_inquiry])
        clean_inquiry = clean_company_info(inquiry)
        return clean_inquiry
            
    except requests.RequestException as e:
        logger.error(f'Search failed: {e}')
        return 'Unable to complete'


def company_info_day(symbol:str):
    '''
        Function that uses a ticker symbol to submit an API call for daily information from the company.
    '''
    quote = daily_activity(symbol)
    if isinstance(quote, pd.DataFrame):
        data = pd.DataFrame.from_dict(quote)
        data = data.infer_objects().reset_index().rename(columns={'index':'Date'})
        success = load_daily_data(symbol, data)
        if success:
            logger.info(f'Data for {symbol} added to db')
        return data
    else:
        print(f'Unable to open file: Filetype: {type(quote)}')


def submit_historic_inquiry(symbol:str, period=str):
    '''
        Function that submits a local and external call to find a weekly or monthly information from a company.
    '''
    try:
        df = quote_historic_data(symbol, period) 
        if df == None:
            return 'Unable to complete API call'
        data = clean_stock(df, period)
        load_periodic_data(symbol, period, data)
        logger.info(f'{period} Data for {symbol} fetched')
        return 'Data uploaded successfully!'
    
    except requests.RequestException as e:
        logger.error(f' Search failed: {e}')
        return 'Unable to complete'
    
    
def dashboard_views(symbol:str, frequency:str):
    '''
        Function that will generate 4 interactive Plotly charts for a given symbol and frequency.
    '''
    conn = connect_db()
    
    # View with Price and Volume Trend
    price_query = '''
        SELECT p.date, p.close, p.volume
        FROM periodic_metrics as p
        JOIN companies as c ON p.company_id = c.id
        WHERE c.symbol = ?
        ORDER BY p.date
    '''
    df_price = pd.read_sql(price_query, conn, params=(symbol,))
    fig_price = px.line(df_price, x='date', y='close', template='ggplot2',
                        title=f'{frequency.title()} Price Trend')
    fig_volume = px.bar(df_price, x='date', y='volume',
                        title='Trading Volume', opacity=0.9)
    
    # View with change in price and distribution
    price_change = '''
        SELECT p.return, p.price_change
        FROM periodic_metrics as p
        JOIN companies as c ON p.company_id = c.id
        WHERE c.symbol = ?
    '''
    df_change = pd.read_sql(price_change, conn, params=(symbol,))
    fig_change_dist = px.histogram(df_change, x='return', nbins=25, template='simple_white',
                                   title=f'{symbol}: {frequency.title()} Price & Return Distribution', opacity=0.8)
    fig_price_box = px.box(df_change, x='price_change', title='Price Change Spread', template='simple_white')
    
    # View with average price range and adjusted close
    avg_price = '''
        SELECT p.range, p.adjusted_close, p.date
        FROM periodic_metrics as p
        JOIN companies as c ON p.company_id = c.id
        WHERE c.symbol = ?
    '''
    df_avg = pd.read_sql(avg_price, conn, params=(symbol,))
    fig_avg_close = px.scatter(df_avg, x='date', y='adjusted_close',
                               color='range', title=f'{symbol}: Price range vs Adjusted Close',
                               )
    fig_avg_close.update_traces(marker=dict(size=8, opacity=0.7))
    
    #View with direction summary
    direction_price = '''
        SELECT p.price_dir, COUNT(*) AS count
        FROM periodic_metrics as p
        JOIN companies as C ON p.company_id = c.id
        WHERE c.symbol=?
        GROUP BY p.price_dir
    '''
    
    df_dir = pd.read_sql(direction_price, conn, params=(symbol,))
    fig_dir = px.pie(df_dir, names='price_dir', values='count', template='seaborn',
                     title=f'{symbol}: Count {frequency.title()} Price Direction')
    
    conn.close()
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_price, width='stretch')
        st.plotly_chart(fig_change_dist, width='stretch',)
        
    with col2:
        st.plotly_chart(fig_volume, width='stretch')
        st.plotly_chart(fig_price_box, width='stretch')
        
    st.plotly_chart(fig_avg_close, width='stretch')
    st.plotly_chart(fig_dir, width='content', theme=None)
    
    
def heatmap_companies():
    
    conn = connect_db()
    market_cap = '''
        SELECT c.market_cap, c.sector, c.symbol, c.previous_close, c.market_sentiment
        FROM companies as c
    '''
    
    df_cap = pd.read_sql(market_cap, conn)
    fig_cap = px.treemap(df_cap, path=['sector', 'symbol', 'previous_close'],
                         values='market_cap', color='market_sentiment', 
                         title='Market sentiment and sector', hover_data='market_cap')
    
    conn.close()
    st.plotly_chart(fig_cap)
    
    
def call_and_update():
    pass
    conn = connect_db()
    symbols = '''
        SELECT c.symbol
        FROM companies as c
        
    '''
    df_companies = pd.read_sql(symbols, conn)
    companies_symbols = df_companies['symbol'].tolist()
    queue = refresh_company_data(companies_symbols)
    new_data = pd.DataFrame(queue.copy())
    print(new_data.columns.get_level_values(0))
    print(new_data.columns.to_numpy())
    return new_data
    # if queue:
    #     True
        
    # else:
    #     False