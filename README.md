## Financial Dashboard 📊

## Overview 
An interactive financial dashboard built with Streamlit that displays key company metrics, tracks performance over time, and highlights potential trends.
Enriched with custom metrics and rendered visualizations through Plotly, it's a hybrid application which pulls and stores locally in SQLite for fast querying.

Data is mix fetched from a yfinance and Alpha Vantage <img width="28" height="28" align="right" alt="www alphavantage" src="https://github.com/user-attachments/assets/caa59cf9-1d08-4e74-bb04-fa83bd4caeb6" />

--
## Key Objectives
- Project end to end utilizing python to create and structure application.
- Create and manage database through SQL usage.
- Implementation of different visualizations dynamically plotting company trend.

--
## Project Structure
Financial_dashboard/
│
├── data_ingestion/
│   ├── __init__.py          # Makes the directory a Python package
│   ├── fetch_data.py        # Script to fetch raw financial data (API/CSV/Excel)
│   ├── clean_data.py        # Transform, validate, preprocess data
│   └── load_data.py         # Insert/update data into SQLite
│
├── db/
│   ├── schema.sql           # SQL schema definition for tables
│   └── financial_data.db    # SQLite database file
│
├── dashboard/
│   ├── __init__.py         
│   └── queries.py           # Helper functions to query data
│
├── utils/
│   ├── __init__.p    
│   ├── db_connection.py     # Config (e.g., DB path, API keys)
│   └── metrics.py           # Agreggated metrics to data ingested
│
├── app.py                   # Main dashboard (Streamlit/Dash/Plotly)
├── requirements.txt         # Python dependencies
└── README.md                # Documentation


## Author
**Steve Hernandez**  
📧 [steve.hernamont@gmail.com] | 🔗 [[LinkedIn](https://www.linkedin.com/in/sthermon/)] | 🌐 []  

---


## How to Run
1. Clone this repo
2. Install requirements:
   ```bash
   pip install -r requirements.txt


   # 📈 financial_dashboard

---
