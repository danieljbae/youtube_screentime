import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
from datetime import date, datetime
import sqlite3
import pandas as pd

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

    ### Adding columns to dataframe for callback functions to filter dateframe
    hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    df['hour_int'] = [int(row) for row in df['hour']]
    cols = ['month', 'dayNum', 'year']
    df['day'] = df[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)
    df['date'] = [datetime.strptime(row, '%b-%d-%Y') for row in df['day']]
    df['weekNum'] = [row.isocalendar()[1] for row in df['date']] 


    ##############################
    ### Dashboard
    ##############################
    app.title = "YouTube Screen Time"
    app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        
        #### Title
        html.H1(
            children='YouTube Screen Time',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        #### App Description
        html.H4(
            children =f'''Categories of YouTube videos watched''',
            style ={
                'textAlign': 'left',
                'color': colors['text']
            }
        ),

        #### Date selection caption to display 
        html.H6(
            id = "date-caption",
            style ={
                'textAlign': 'left',
                'color': 'whitesmoke'
            }
        ),

        #### Date Picker Component filtering graph data
        html.Div([
            dcc.DatePickerSingle(
                id='my-date-picker-single',
                min_date_allowed=date(2020, 9, 1),
                max_date_allowed=date(2020, 10, 4),
                initial_visible_month=date(2020, 8, 5),
                date=date(2020, 9, 1)
            ),
            html.Div(id='output-container-date-picker-single')
        ]),
        

        #### Tab Component containing graphs
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='This Week', children=[
                    dcc.Graph(
                        id = 'weekly-graph'
                    )
                ]),
                dcc.Tab(label='Today', children=[
                    dcc.Graph(
                        id = 'daily-graph'
                    )
                ]),
            ],colors={
                "border": colors["tab_border"],
                "primary": colors["tab_primary"],
                "background": colors["tab_background"]
                })
        ])
    ])



    ##############################
    ### Updating Graphs per input 
    ############################## 
    @app.callback(
        dash.dependencies.Output('daily-graph', 'figure'),
        dash.dependencies.Output('weekly-graph', 'figure'),
        dash.dependencies.Output('date-caption', 'children'),
        dash.dependencies.Output('output-container-date-picker-single', 'children'),
        [dash.dependencies.Input('my-date-picker-single', 'date')])

    def update_output(date_value):

        string_prefix = 'You have selected: '
        date_caption_prefix = "Videos watched during the week of: "
        if date_value is not None:
            date_object = date.fromisoformat(date_value)
            date_string = date_object.strftime('%B %d, %Y')


            ### Weekly Graph
            chosenWeekNumber = datetime.strptime(date_value, '%Y-%m-%d').isocalendar()[1]
            df_thisWeek = df.loc[df["weekNum"] == chosenWeekNumber]
            grouped_df = pd.DataFrame(df_thisWeek.groupby(['dayName', 'categoryName']).count()).reset_index()
            grouped_df = grouped_df.iloc[:, 0:3].rename(columns={"videoID": "count"})
            figWeek = px.bar(grouped_df, x="dayName", color="categoryName",
                        y='count',
                        title=f"YouTube videos watched: This Week",
                        barmode='stack',
                        height=700
                        )
            figWeek.update_layout(xaxis={"title": "Day"},yaxis={'title':"# of Videos Watched"})
            figWeek.update_xaxes(categoryorder='array',categoryarray= ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'])
            figWeek.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text']
            ) 

            ### Daily Graph
            chosenDay = datetime.strptime(date_value, '%Y-%m-%d')
            df_today = df.loc[df["date"] == chosenDay]
            grouped_df = pd.DataFrame(df_today.groupby(['hour_int', 'categoryName']).count()).reset_index()
            grouped_df = grouped_df.iloc[:, 0:3].rename(columns={"videoID": "count"})
            figDay = px.bar(grouped_df, x="hour_int", color="categoryName",
                        y='count',
                        title="YouTube videos watched: Today",
                        barmode='stack',
                        height=700  
                        )
            figDay.update_layout(xaxis={"title": "Hours"},yaxis={'title':"# of Videos Watched"})
            figDay.update_xaxes(categoryorder='array',categoryarray= hours,tickvals=[0, 6, 12, 18, 24])
            figDay.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text']
            )


            return figDay,figWeek,date_caption_prefix + date_string,string_prefix + date_string

    if __name__ != '__main__':
        app.run_server(debug=True)