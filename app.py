import streamlit as st
from dashboard.queries import get_company_info, process_results, submit_selection
from data_ingestion.load_data import retrieve_company_data, retrieve_periodic_data
from data_ingestion.fetch_data import quote_data, quote_historic_data
from utils.db_connection import init_db, connect_db

init_db()
def get_db_connection():
    return connect_db()

st.title("📈 Financial Dashboard")

st.write('-------')
# st.session_state
st.write('Enter company ticker or Symbol:')
query = st.text_input(' ', placeholder='Enter a company ticker (e.g., AAPL, MSFT, TSLA):', key='search', max_chars=20, width=500)
# user_clicked = st.button('Search')

if query:
    with st.spinner('Fetching results...'):
        print(f'Passing the values {query}')
        lookup_company = quote_data(query)
        options = [f'{i}. {company.longname} - ({company.symbol}) -  {company.typeDisp}'
                   for i, (company) in enumerate(lookup_company, 1)]
        
        prompt = st.selectbox('Please select the ticker company: ', options, width=500, key='select')
        
        selected_company = lookup_company[prompt - 1]
        symbol = selected_company.symbol
        
        if prompt:
            dossier = get_company_info(symbol)
            st.table(dossier)
        
        # if result:
        #     st.success(f'✅ Fetching {query} overview.')
        #     dossier = submit_selection(symbol=symbol)
        #     st.table(dossier)
        #     weekly = retrieve_periodic_data(symbol)
        #     st.data_editor(weekly)
        #     if not weekly:
        #         st.error('Company not found ⚠️')
        #     st.spinner('Loading company data')
        #     db_data = retrieve_company_data(symbol)
        #     st.table(db_data)
        # else: 
# else:
    # st.error('Company not found ⚠️')
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
