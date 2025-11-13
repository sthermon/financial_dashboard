## Financial Dashboard 📊

## Overview 
An interactive **financial dashboard** built with **Streamlit** that displays key company metrics, tracks performance over time, and visualizes potential trends.  
The app combines **real-time API data** with **locally stored insights in SQLite** for fast querying and dynamic analytics.  

---
## Key features:
- Interactive company search and dossier view  
- Custom-calculated metrics (price range, returns, average price, etc.)  
- Multiple frequency tracking (daily, weekly, monthly)  
- Dynamic Plotly visualizations for trend exploration  
- Persistent local database caching for efficient performance 

Data is fetched from **Yahoo Finance (yfinance)** and **Alpha Vantage** APIs.  
<img width="28" height="28" align="right" alt="Alpha Vantage logo" src="https://github.com/user-attachments/assets/caa59cf9-1d08-4e74-bb04-fa83bd4caeb6" />

## Key Objectives

- Develop a **fully functional Python application** for financial data analysis.  
- Design and manage a **SQLite database schema** for structured storage.  
- Integrate **data ingestion, transformation, and visualization** into one cohesive pipeline.  
- Implement multiple **Plotly charts** that dynamically reflect a company’s market behavior.  

---
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
1. **Clone this repository**
2. Install requirements:
   ```bash
   git clone https://github.com/sthermon/financial_dashboard.git
   pip install -r requirements.txt
   cd financial_dashboard

📈 [financial_dashboard] (https://github.com/sthermon/financial_dashboard.git)
---
