import sqlite3
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DB_PATH = Path(__file__).resolve().parent.parent / 'db' / 'financial_data.db'
SCHEMA = Path(__file__).resolve().parent.parent / 'db' / 'schema.sql'

def connect_db():
    
    return sqlite3.connect(DB_PATH)    
        
def init_db():
    
    connection = sqlite3.connect(DB_PATH)
    with open(SCHEMA, 'r') as f:
        schema_sql = f.read()
    connection.executescript(schema_sql)
    connection.commit()
    connection.close()
    print('Database initialized')

