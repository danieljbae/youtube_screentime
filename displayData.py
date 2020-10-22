# import plotly.express as px
# import plotly.graph_objs as go
# import dash
# import dash_core_components as dcc
# import dash_html_components as html

import sqlite3
import pandas as pd
import plotly.express as px


def plot_data(df):
    """
    Create plotly chart(s)
    """
        
    grouped_df = pd.DataFrame(df.groupby(['dayName', 'categoryName']).count()).reset_index()
    grouped_df = grouped_df.iloc[:, 0:3].rename(columns={"videoID": "count"})

    fig = px.bar(grouped_df, x="dayName", color="categoryName",
                y='count',
                title="YouTube Videos Watched per Category",
                barmode='stack',
                height=1000,
                #  category_orders={"dayName": ["Thur", "Fri", "Sat", "Sun"]}
                )

    fig.update_layout(xaxis={"title": "Day"},yaxis={'title':"# of Videos Watched"})
    fig.update_xaxes(categoryorder='array',categoryarray= ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'])
    fig.show()
    