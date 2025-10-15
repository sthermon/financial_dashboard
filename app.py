import streamlit as st
from streamlit_searchbox import st_searchbox
from dashboard import get_company_info, rank_results
# from data_ingestion import pull_company_data
# from data_ingestion import clean_stock

st.title("📈 Financial Dashboard")

ticker = st_searchbox("Enter a company ticker:", "AAPL")

def search_company(searchterm):
    
    return searchterm if searchterm else []

selected_company = st_searchbox(
    search_function=search_company,
    placeholder="Enter a company ticker:...",
    key='ticker',
    min_execution_time=10
)

if selected_company:
    with st.spinner('Searching company...'):
        result = get_company_info(ticker)
        rank = rank_results(ticker, result)

    if rank:
        st.success(f"✅ Found {ticker} in database.")
        
    else:
        st.warning(f"⚠️ {ticker} not found, fetching from API...")
        # raw = fetch_financial_data(symbol)
        # cleaned = clean_stock(raw)
        # load_financial_data(cleaned, symbol)
        st.success(f"📥 Data for {ticker} saved to database.")

    # Always query locally (fast!)
    # df = company_check(symbol)
    # st.line_chart(df.set_index("date")[["revenue", "profit", "stock_price"]])
    # st.dataframe(df.tail(10))
