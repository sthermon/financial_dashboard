import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox
from dashboard import get_company_info, process_results
from data_ingestion import pull_company_data
# from data_ingestion import clean_stock

st.title("📈 Financial Dashboard")

def search_button(search:str):
    
    result = get_company_info(search)
    return result

query = st.text_input('Enter search term: ')

if query:
    with st.spinner('Fetching results...'):
        result = search_button(query)
        best_match, score = process_results(query, result)
        
        # st.table(result)
        st.write(best_match)
        st.write(score)
        
        if best_match and score > 70:
            st.success(f'✅ Found {query} in database.')
            st.spinner('Loading company data')

            st.write('The best match is: {best_match}, symbol is {symbol}, with a score of {score}')
        
        elif best_match:
            st.info("No strong match found. Try refining your input.")
        else:
            st.warning("No results returned from API.")
                
            # dossier = pull_company_data(symbol)
            # st.table(pd.read_json(dossier))
            # selected_company = st_searchbox(
#     search_function=search_button(ticker),
#     placeholder="Enter a company ticker:",
#     # key='ticker',
#     min_execution_time=10
# )

# if selected_company:
#     with st.spinner('Searching company...'):
#         st.write(f'selected {selected_company}')
#         # rank = rank_results(ticker, result)

#     if result:
#         st.success(f"✅ Found {ticker} in database.")
        
#     else:
#         st.warning(f"⚠️ {ticker} not found, fetching from API...")
        # raw = fetch_financial_data(symbol)
#         # cleaned = clean_stock(raw)
#         # load_financial_data(cleaned, symbol)
#         st.success(f"📥 Data for {ticker} saved to database.")

    # Always query locally (fast!)
    # df = company_check(symbol)
    # st.line_chart(df.set_index("date")[["revenue", "profit", "stock_price"]])
