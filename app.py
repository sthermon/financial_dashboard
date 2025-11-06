import streamlit as st
from dashboard.queries import get_company_info, company_info_day, submit_historic_inquiry
from data_ingestion.fetch_data import quote_data
from utils.db_connection import init_db, connect_db

init_db()
def get_db_connection():
    return connect_db()

st.title("📈 Financial Dashboard")

st.write('-------')
# st.session_state
st.write('Enter company ticker or Symbol:')
query = st.text_input(' ', placeholder='Enter a company ticker (e.g., AAPL, MSFT, TSLA):', key='search', max_chars=20, width=500)
user_clicked = st.button('Search')

if query:
    with st.spinner('Fetching results...'):
        print(f'Passing the values for {query}')
        lookup_company = quote_data(query)
        options = [f'{i}. {company.symbol} - {company.longname} - ({company.typeDisp})'
                   for i, company in enumerate(lookup_company, 1)]
        
        selected_option = st.selectbox('Please select the ticker company: ', options, width=500, key='select')
        prompt = int(selected_option[0])
        selected_company = lookup_company[prompt - 1]
        symbol = selected_company.symbol
        
        if prompt:
            daily_quote = st.dataframe(company_info_day(symbol))
            dossier = st.dataframe(get_company_info(symbol))
            
            first_batch = submit_historic_inquiry(symbol)
            batch = st.dataframe(first_batch)
            # st.subheader("Daily data")
            # st.table(daily_quote)

            # st.subheader("Company info")
            # st.table(dossier)
            
        else:
            st.error('Company not found ⚠️')
        #     st.success(f'✅ Fetching {query} overview.')
#         st.success(f"📥 Data for {ticker} saved to database.")
            