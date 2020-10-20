# import plotly.express as px
# import plotly.graph_objs as go
# import dash
# import dash_core_components as dcc
# import dash_html_components as html

import sqlite3
import pandas as pd

def load_data(db_filename,table_name):
    """
    Load data from database
    """
    conn = sqlite3.connect(db_filename) 
    table_name = 'VIDEOS'
    df = pd.read_sql(f"select * from {table_name}", con=conn)
    return df 

def plot_data(db_filename,table_name):
    """
    Create plotly chart(s)
    """
    df = load_data(db_filename,table_name)
    print(df.head())
    