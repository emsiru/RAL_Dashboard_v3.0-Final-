import dash_bootstrap_components as dbc
from dash import dash, Input, Output, State, html, dcc
import pymysql
import time
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from app import app

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id = 'torque-graph', figure = {}),
                            dcc.Interval(id = 'graph-update', n_intervals = 0, interval = 1000*1)
                        ])
                    ]),

                    dbc.Row([
                        dbc.Col([
                            html.Div('% Change: ', style = {'size':20})
                        ], width = 1, className = 'ms-5'),

                        dbc.Col([
                            html.Div([
                                dcc.Graph(id = 'delta-indicator', figure = {}),
                                dcc.Interval(id = 'delta-update', n_intervals = 0, interval = 1000*1)
                            ], style = {'width':'12rem'})
                        ])
                    ]),
                ])
            ], style = {'width' : '145rem'}, className = 'm-5', color = '#1f2c56', inverse=True)
        ])
    ], justify='center')
], fluid = True, 
    style = {'backgroundColor':'#0c1840'},
    className = 'p-5')

# Delta indicator callback
@app.callback(
    Output('delta-indicator', 'figure'),
    Input('delta-update', 'n_intervals')
)
def update_delta(timer):
    for seconds in range(5):
        mydb2 = pymysql.connect(
            host="192.168.0.207",
            user="Emmanuel_Sim",
            password= "1221",
            database = "ral_dashboard"
        )
        cursor2 = mydb2.cursor()
        data = {
            "Torque":[],
            "Time":[]
            }
        cursor2.execute("SELECT * FROM s3_smart_drill_torque ORDER BY PID DESC LIMIT 30")
        # SELECT * FROM ( SELECT * FROM s3_smart_drill_torque ORDER BY PID DESC LIMIT 3 )Var1 ORDER BY time_stamp ASC

        tmp = cursor2.fetchall()
        mydb2.commit()

        for i in range(len(tmp)):
            data['Torque'].append(tmp[i][2])
            data['Time'].append(tmp[i][1])

        # mydb2.close()
        df1 = pd.DataFrame(data)
        df1['Time'] = pd.to_datetime(df1['Time'],format).apply(lambda x: x.time())
        df1=df1.iloc[::-1]
        mydb2.close()
    
    dff_rv = df1.iloc[::-1]
    day_start = dff_rv[dff_rv['Time'] == dff_rv['Time'].min()]['Torque'].values[0]
        
    day_end = dff_rv[dff_rv['Time'] == dff_rv['Time'].max()]['Torque'].values[0]


    fig = go.Figure(go.Indicator(
        mode = 'delta',
        value = day_end,
        delta = {'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font = {'size':13})
    fig.update_layout(height = 30, width = 80)
    fig.update_layout({
    'paper_bgcolor': '#1f2c56'
    })

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='#11fa30')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='#d14952')

    return fig




@app.callback(
    Output('torque-graph', 'figure'),
    Input('graph-update', 'n_intervals')
)
def update_graph(n):
    for seconds in range(5):
        mydb = pymysql.connect(
            host="192.168.0.207",
            user="Emmanuel_Sim",
            password= "1221",
            database = "ral_dashboard"
        )

        cursor = mydb.cursor()
        cursor2 = mydb.cursor()

        data = {
            "Torque":[],
            "Temperature":[],
            "Time":[]
            }
        cursor.execute("SELECT * FROM s3_smart_drill_torque ORDER BY PID DESC LIMIT 30")
        cursor2.execute("SELECT * FROM temperature ORDER BY PID DESC LIMIT 30")
        # SELECT * FROM ( SELECT * FROM s3_smart_drill_torque ORDER BY PID DESC LIMIT 3 )Var1 ORDER BY time_stamp ASC

        tmp = cursor.fetchall()
        tmp2 = cursor2.fetchall()
        mydb.commit()

        for i in range(len(tmp)):
            data['Torque'].append(tmp[i][2])
            data['Time'].append(tmp[i][1])
            data['Temperature'].append(tmp2[i][1])
        
        df1 = pd.DataFrame(data)
        df1['Time'] = pd.to_datetime(df1['Time'],format).apply(lambda x: x.time())
        df1=df1.iloc[::-1]
        mydb.close()
        
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(go.Scatter(x= df1['Time'], y=df1['Torque'], mode='lines+markers'), secondary_y=False)
    #fig.add_trace(go.Scatter(y=data['Torque'], x=data['Time'], mode="lines+markers"), row=1, col=1)
    fig.update_layout(title = {'text':'Smart Drill Torque and Temperature VS Time', 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    fig.update_xaxes(title = 'Time (s)')
    fig.update_yaxes(title = 'Torque (Nm)', range = [0,0.2], secondary_y = False)
    fig.update_layout(font=dict(color='#ffffff'))
    fig.update_layout(paper_bgcolor='#1f2c56', plot_bgcolor='#1f2c56',)
    fig.update_traces(marker_color='#d14952')
    fig.update_traces(marker_color='#d14952', name = 'Torque', secondary_y=False)

    fig.add_trace(
        go.Scatter(x=df1['Time'], y=df1['Temperature'], mode = 'lines+markers', name = 'Temperature'),
        secondary_y=True,
    )

    fig.update_yaxes(title = 'Temperature (C)', range = [50,60], secondary_y = True)
    fig.update_traces(marker_color='#11fa30', secondary_y=True)
    return fig


# if __name__ == '__main__':
#     app.run_server(debug=False, port = 3000)