import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


from datetime import date, datetime
import sqlite3
import pandas as pd
import plotly.express as px


# currentWeek = date.today().isocalendar()[1] # Current week number (ex. 1 - 52)
# dateToday = date.today().strftime('%m-%d-%Y') # Current Day (ex. 10-10-2020)

today = '10-4-2020'
currentWeekNumber = datetime.strptime(today, '%m-%d-%Y').isocalendar()[1] # sample, ran out of quota on API
dateToday = datetime.strptime(today, '%m-%d-%Y') # sample, ran out of quota on API


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    "tab_border": "dimgrey",
    "tab_primary": "dimgrey",
    "tab_background": "darkgrey"
    }


def plot_data(df):
    """
    Create plotly chart(s)
    """

    ### Videos from this week and Videos from today
    hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    df['hour_int'] = [int(row) for row in df['hour']]

    cols = ['month', 'dayNum', 'year']
    df['day'] = df[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)
    df['date'] = [datetime.strptime(row, '%b-%d-%Y') for row in df['day']]
    df['weekNum'] = [row.isocalendar()[1] for row in df['date']] 
    df_thisWeek = df.loc[df["weekNum"] == currentWeekNumber]
    df_today = df.loc[df["date"] == dateToday]
    
    ### Weekly plot 
    grouped_df = pd.DataFrame(df_thisWeek.groupby(['dayName', 'categoryName']).count()).reset_index()
    grouped_df = grouped_df.iloc[:, 0:3].rename(columns={"videoID": "count"})
    figWeek = px.bar(grouped_df, x="dayName", color="categoryName",
                y='count',
                title=f"YouTube videos watched: This Week",
                barmode='stack',
                height=800
                )  

    figWeek.update_layout(xaxis={"title": "Day"},yaxis={'title':"# of Videos Watched"})
    figWeek.update_xaxes(categoryorder='array',categoryarray= ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'])
    

    figWeek.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )


    ### Daily plot
    grouped_df = pd.DataFrame(df_today.groupby(['hour_int', 'categoryName']).count()).reset_index()
    grouped_df = grouped_df.iloc[:, 0:3].rename(columns={"videoID": "count"})
    figDay = px.bar(grouped_df, x="hour_int", color="categoryName",
                y='count',
                title="YouTube videos watched: Today",
                barmode='stack',
                height=800
                )

    figDay.update_layout(xaxis={"title": "Hours"},yaxis={'title':"# of Videos Watched"})
    figDay.update_xaxes(categoryorder='array',categoryarray= hours,tickvals=[0, 6, 12, 18, 24])
    # figDay.show()



    ### Dashboard
    app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
            children='YouTube Screen Time',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        
        ),
        
        html.H4(
            children =f'''Categories of YouTube videos watched''',
            style ={
                'textAlign': 'left',
                'color': colors['text']
            }
        ),

        html.H6(
            children =f'''Videos watched during the week of: {today}''',
            style ={
                'textAlign': 'left',
                'color': 'whitesmoke'
            }
        ),

        html.Div([
            dcc.Tabs([
                dcc.Tab(label='This Week', children=[
                    dcc.Graph(
                        figure=figWeek
                    )
                ]),
                dcc.Tab(label='Today', children=[
                    dcc.Graph(
                        figure=figDay
                    )
                ]),
            ],colors={
                "border": colors["tab_border"],
                "primary": colors["tab_primary"],
                "background": colors["tab_background"]
                })
        ])
    ])

    figDay.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )


    if __name__ != '__main__':
        app.run_server(debug=True)