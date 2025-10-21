import streamlit as st
import pandas as pd
from streamlit_searchbox import st_searchbox
from dashboard.queries import get_company_info, process_results, submit_selection
from utils.db_connection import init_db, connect_db, logger
# from data_ingestion.fetch_data import pull_company_data
# from data_ingestion import clean_stock

init_db()
@st.cache_resource
def get_db_connection():
    return connect_db()

st.title("📈 Financial Dashboard")

def search_button(search:str):
    
    result_obj = get_company_info(search)
    return result_obj

query = st.text_input('Enter search term: ')
# st.session_state
if query:
    with st.spinner('Fetching results...'):
        
        result = search_button(query)
        best_matches = process_results(query, result)
        
        options = [f'{i}. {match.name} - ({match.symbol})'
                   for i, (match, score) in enumerate(best_matches, 1)
                ]
        results = {company: (symbol, name) for company, (symbol, name) in zip(options, best_matches)}
        
        selected = st.selectbox('Please select the ticker company: ', options)
        company, _ = results[selected]
        symbol = company.symbol
                
        if selected:
            st.success(f'✅ Fetching {query} overview.')
            dossier = submit_selection(symbol=symbol)
            with st.spinner('Loading company data'):
                st.table(dossier)
        else:
            st.error('Company not found ⚠️')
                
                
                
                # data_load = 

        #     st.write('The best match is: {best_match}, symbol is {symbol}, with a score of {score}')
        
        # elif best_match:
        #     st.info("No strong match found. Try refining your input.")
        # else:
        #     st.warning("No results returned from API.")
                
            # dossier = pull_company_data(symbol)
            # st.table(pd.read_json(dossier))
            # selected_company = st_searchbox(
#     search_function=search_button(ticker),
#     placeholder="Enter a company ticker:",
#     # key='ticker',
#     min_execution_time=10
# )

# matches = get_company_info(user_input)
# top_matches = process_results(user_input, matches, top_n=3)

# if not top_matches:
#     print("No matches found.")
# else:
#     print("Top matches:")
#     for i, (match, score) in enumerate(top_matches, 1):
#         print(f"{i}. {match.name} ({match.symbol}) - Score: {score}")

#     # Let user select (e.g., via input or click)
#     selected_index = int(input("Enter the number of your choice: ")) - 1
#     selected_match = top_matches[selected_index][0]
#     print(f"You selected: {selected_match.name}")


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
