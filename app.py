import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from dashboard.queries import get_company_info, company_info_day, submit_historic_inquiry, dashboard_views
from data_ingestion.fetch_data import quote_data
from utils.db_connection import init_db

init_db()

st.title("📈 Financial Dashboard")
st.divider()
st.subheader('Enter company name or Symbol:')

company = st.text_input(' ', placeholder='e.g., Apple, Tesla / NVDA, MSFT:', key='search', max_chars=20, width=500)

col1, col2 = st.columns(2)
with col1:
    user_clicked = st.checkbox('Search a list of companies',  value=False, key='company_list')
with col2:
    frequency = st.radio(
        'Data frequency',
        ['Weekly', 'Monthly'],
        label_visibility='collapsed',
        key = 'frequency',
        horizontal=True,
        # disabled=st.sesion_state.disabled
)

if company and not user_clicked:
    with st.spinner('Drawing company dossier...'):
        try:
            with st.container():
                folder = st.dataframe(get_company_info((company.upper())))
                company_day = st.dataframe(company_info_day(company.upper()))
                submit_historic_inquiry(company, frequency.lower())
                
            st.subheader(f'{company} {frequency.title()} Performance Overview')
            
            dashboard_views(company.upper(), frequency=frequency.lower())
           
            
        except (KeyError, TypeError, ValueError) as e:
            print(f'Unable to complete search: {e}')
            st.error('company not found, please verify your search.')



if company and user_clicked:
    with st.spinner('Fetching results...'):
        # print(f'Passing the values for {company}')
        lookup_company = quote_data(company)
        if lookup_company:
            options = [f'{i}. {company.symbol} - {company.shortname} - ({company.typeDisp})'
                    for i, company in enumerate(lookup_company, 1)]
            
            selected_option = st.selectbox('Select the company: ', options, width=500, key='selection')
            prompt = int(selected_option[0])
            try:
                with st.container():
                    
                    if prompt:
                        selected_company = lookup_company[prompt - 1]
                        symbol = selected_company.symbol
                        with st.spinner('Fetching company data...'):
                            
                            st.dataframe(get_company_info(symbol))
                            st.dataframe(company_info_day(symbol)) 
                            submit_historic_inquiry(symbol, frequency.lower())
                            
                            st.subheader(f'{company} {frequency.title()} Performance Overview')
            
                            dashboard_views(company.upper(), frequency=frequency.lower())
                            
                            
                            
            except (KeyError, TypeError, ValueError) as e:
                print(f'Unable to complete search: {e}')
                st.error('company not found, please verify your search.')
                            
    # else:
    #     st.error(f'{company} not found, try with other company.⚠️')
                        
# st.session_state.setdefault('selected_symbol', None)
# if st.session_state.selected_symbol != symbol:
#     st.session_state.selected_symbol = symbol
    #st.session_state.frequency = True
