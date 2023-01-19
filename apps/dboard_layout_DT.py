from dash import dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from opcua import Client
import numpy as np
import pymysql
import pandas as pd
from datetime import datetime
import time
# from button import button_card
from app import app


const = datetime(2022, 9, 12, 8, 0, 0, 0) # 8-5

val1 = const.time()

# url = "opc.tcp://192.168.0.80:4840"
# client = Client(url)
# client.connect()

# global temp
# masterkey=client.get_node('ns=2;s=Application.GVL_HMI.bStart_HMI_i  ') #sets START button as ALWAYS ON
# masterkey.get_access_level()
# state=masterkey.get_value()


# masterkey.set_value(True,varianttype=None)
# state=masterkey.get_value()
# key=client.get_node('ns=2;s=Application.GVL_HMI.bInvStop_HMI_i  ') # gets initial state of stop button
# key.get_access_level()
# state=key.get_value()
# temp=state #to set initial button state

# LAYOUT COMPONENTS ---------------------------------------------------------------------------------------------------------------

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

# global db
# global cursor
db=pymysql.connect(
    host= "192.168.0.207",
    user= "Emmanuel_Sim",
    password= "1221",
    database= "ral_dashboard")
cursor=db.cursor()
print("Connected")

cursor=db.cursor()
global data
data={
    "Station":[],
    "Doorlocked_f":[],
    "Doorlocked_b":[],
    "fts_f":[],
    "fts_b":[],
    "Drive":[],
    "Rfid":[],
    "Estop":[],
    "Timestamp":[]
}
cursor.execute(("SELECT * FROM entry ORDER BY PID DESC LIMIT 1"))
testresult=cursor.fetchall()
db.commit()
try:
    for i in range(len(testresult)):
                data['Station'].append("Entry")
                data['Doorlocked_f'].append(testresult[i][1])
                data['Doorlocked_b'].append(testresult[i][1])
                data['fts_f'].append(testresult[i][2])
                data['fts_b'].append(testresult[i][2])
                data['Drive'].append(testresult[i][3])
                data['Rfid'].append(testresult[i][4])
                data['Estop'].append(testresult[i][5])
                data['Timestamp'].append(testresult[i][6])
except Exception as error:
    print("Database is Null")
    print(error)
cursor.execute(("SELECT * FROM dispensing ORDER BY PID DESC LIMIT 1"))
testresult=cursor.fetchall()
db.commit()
try:
    for i in range(len(testresult)):
                data['Station'].append("Dispensing")
                data['Doorlocked_f'].append(testresult[i][1])
                data['Doorlocked_b'].append(testresult[i][2])
                data['fts_f'].append(testresult[i][3])
                data['fts_b'].append(testresult[i][4])
                data['Drive'].append(testresult[i][5])
                data['Rfid'].append(testresult[i][6])
                data['Estop'].append(testresult[i][7])
                data['Timestamp'].append(testresult[i][8])
                
except Exception as error:
    print("Database is Null")
    print(error)
print("Connected")
cursor.execute(("SELECT * FROM tightening ORDER BY PID DESC LIMIT 1"))
testresult=cursor.fetchall()
db.commit()
try:
    for i in range(len(testresult)):
                data['Station'].append("Pick and place")
                data['Doorlocked_f'].append(testresult[i][1])
                data['Doorlocked_b'].append(testresult[i][2])
                data['fts_f'].append(testresult[i][3])
                data['fts_b'].append(testresult[i][4])
                data['Drive'].append(testresult[i][5])
                data['Rfid'].append(testresult[i][6])
                data['Estop'].append(testresult[i][7])
                data['Timestamp'].append(testresult[i][8])
                
except Exception as error:
    print("Database is Null")
    print(error)
cursor.execute(("SELECT * FROM pickandplace ORDER BY PID DESC LIMIT 1"))
testresult=cursor.fetchall()
db.commit()
try:
    for i in range(len(testresult)):
                data['Station'].append("Tightening")
                data['Doorlocked_f'].append(testresult[i][1])
                data['Doorlocked_b'].append(testresult[i][2])
                data['fts_f'].append(testresult[i][3])
                data['fts_b'].append(testresult[i][4])
                data['Drive'].append(testresult[i][5])
                data['Rfid'].append(testresult[i][6])
                data['Estop'].append(testresult[i][7])
                data['Timestamp'].append(testresult[i][8])
                
except Exception as error:
    print("Database is Null")
    print(error)
cursor.execute(("SELECT * FROM exit_station ORDER BY PID DESC LIMIT 1"))
testresult=cursor.fetchall()
db.commit()
try:
    for i in range(len(testresult)):
                data['Station'].append("Exit")
                data['Doorlocked_f'].append(testresult[i][1])
                data['Doorlocked_b'].append(testresult[i][1])
                data['fts_f'].append(testresult[i][2])
                data['fts_b'].append(testresult[i][2])
                data['Drive'].append(testresult[i][3])
                data['Rfid'].append(testresult[i][4])
                data['Estop'].append(testresult[i][5])
                data['Timestamp'].append(testresult[i][6])
except Exception as error:
    print("Database is Null")
    print(error)
global df
df = pd.DataFrame(data)
df['Timestamp'] = pd.to_datetime(df['Timestamp'],format).apply(lambda x: x.time()) #remove date, keep time only
df=df.iloc[::-1] #orders time from oldest to latest
df.loc[df['Doorlocked_f'] == 2, 'Doorlocked_f'] = "Closed" #changes value of doorstate to strings
df.loc[df['Doorlocked_f'] == 1, 'Doorlocked_f'] = "Open"
df.loc[df['Doorlocked_b'] == 2, 'Doorlocked_b'] = "Closed"
df.loc[df['Doorlocked_b'] == 1, 'Doorlocked_b'] = "Open"
df.loc[df['Drive'] == 'Ab', 'Drive'] = "Initializing"
df.loc[df['Drive'] == 'AF', 'Drive'] = "Running"
df.loc[df['Drive'] == 'Fatal', 'Drive'] = "Error"
df.loc[df['Rfid'] == 1, 'Rfid'] = "Working"
df.loc[df['Rfid'] == 0, 'Rfid'] = "Error"
df.loc[df['Estop'] == 1, 'Estop'] = "Working"
df.loc[df['Estop'] == 0, 'Estop'] = "Error"
df["Door"] = df['Doorlocked_f'].astype(str) +"\n"+ df["Doorlocked_b"]
df["Fts"] = df['fts_f'] +"\n"+ df["fts_b"]
df=df.drop(columns=['Doorlocked_f','Doorlocked_b'])
df=df.drop(columns=['fts_f','fts_b'])
df.loc[df['Door'] == "Open\nClosed", 'Door'] = "Front (Open)\nBack (Closed)"
df.loc[df['Door'] == "Open\nOpen", 'Door'] = "Front (Open)\nBack  (Open)"
df.loc[df['Door'] == "Closed\nClosed", 'Door'] = "Front (Closed)\nBack (Closed)"
df.loc[df['Door'] == "Closed\nOpen", 'Door'] = "Front (Closed)\nBack (Open)"
df['Door'] = np.where((df['Door'] == "Front (Closed)\nBack (Closed)") & (df['Station'] == 'Entry'), "Front (Closed)", df['Door'])
df=df[['Station','Door','Fts','Drive','Rfid','Estop','Timestamp']]
df = df.sort_index(ascending=True)
print(df)


card = dbc.Card(
    [dbc.CardHeader("Header"), dbc.CardBody("Body")], className="h-100", color = '#1f2c56'
)


piechart_card = dbc.Card([
    dbc.CardHeader("Overall Equipment Effectiveness Piechart Distributions"), 
    dbc.CardBody([ 
        dbc.Row([ 
            dbc.Col([ 
                dcc.Graph(id = 'piecharts')
            ]),
        ]),
        dcc.Interval(id = 'piechart-interval', interval = 1*1000, n_intervals=0)
    ], className="h-100")
], inverse=True, color = '#1f2c56')

bar_card = dbc.Card([
    dbc.CardHeader("Temperature Bar Chart"), 
    dbc.CardBody([ 
        dbc.Row([ 
            dbc.Col([ 
                dcc.Graph(id = 'barchart')
            ]),
        ]),
        dcc.Interval(id = 'barchart-interval', interval = 1*1000, n_intervals=0)
    ], className="h-100")
], inverse=True, color = '#1f2c56')

graph_card = dbc.Card([
    dbc.CardHeader("STATION STATUS", style = {'color':'white'}), 
    dbc.CardBody([ 
        dbc.Row([ 
            dbc.Col([ 
                html.H4([
                        dash_table.DataTable(
                            id='table',
                            data=df.to_dict('records'),
                            columns=[
                                {'name': i, 'id': i} for i in df.columns
                            ], 
                            style_header={
                            'border': '1px solid black',
                            'textAlign': 'center'},
                            style_cell={
                            'border': '2px solid black',
                            'whiteSpace': 'pre-line',
                            'textAlign': 'center',
                            'font_size':'15px',
                            'font_family':'Open Sans'},
                            style_data_conditional=(
                            [
                                {
                                    'if': {'column_id': 'Station'},
                                'width': '10%'
                                }
                            ]
                            +
                            [
                                {
                                    'if': {'column_id': 'Door'},
                                'width': '10%'
                                }
                            ]
                            +
                            [
                                {
                                    'if': {'column_id': 'Fts'},
                                'width': '10%'
                                }
                            ]
                            +
                            [
                                {
                                    'if': {'column_id': 'Drive'},
                                'width': '10%'
                                }
                            ]
                            +
                            [
                                {
                                    'if': {'column_id': 'Rfid'},
                                'width': '10%'
                                }
                            ]
                            +
                            [
                                {
                                    'if': {'column_id': 'Estop'},
                                'width': '10%'
                                }
                            ]
                            +
                            [
                                {
                                    'if': {'column_id': 'Timestamp'},
                                'width': '10%'
                                }
                            ]
                            +
                            [
                                {
                                'if': {
                                    'filter_query': '{{{}}} contains "Error"'.format(col),
                                    'column_id': col
                                },
                                'backgroundColor': '#FF0000', #Error
                                'color': 'white'
                                } for col in df.columns
                            ]
                            +
                            [
                                {
                                'if': {
                                    'filter_query': '{{{}}} contains "Locked"'.format(col),
                                    'column_id': col
                                },
                                'backgroundColor': '#3D9970', #green
                                'color': 'white'
                                } for col in df.columns
                            ]
                                +
                            [
                                {
                                'if': {
                                    'filter_query': '{{{}}} contains "Active"'.format(col),
                                    'column_id': col
                                },
                                'backgroundColor': '#3D9970', #green
                                'color': 'white'
                                } for col in df.columns
                            ] 
                                +
                            [
                                {
                                'if': {
                                    'filter_query': '{{{}}} contains "Unlocked"'.format(col),
                                    'column_id': col
                                },
                                'backgroundColor': '#FF0000', #red
                                'color': 'white'
                                } for col in df.columns
                            ]
                                +
                            [
                                {
                                'if': {
                                    'filter_query': '{{{}}} contains "Idle"'.format(col),
                                    'column_id': col
                                },
                                'backgroundColor': '#FFBD33', #yellow
                                'color': 'white'
                                } for col in df.columns
                            ]
                                +
                                [{
                                    'if': {
                                        'filter_query': '{Drive} contains "Working"',
                                        'column_id': 'Drive'
                                        },
                                    'backgroundColor': '#3D9970', #green
                                    'color': 'white'
                                }]
                                +
                                [{
                                    'if': {
                                        'filter_query': '{Drive} contains "Initializing"',
                                        'column_id': 'Drive'
                                        },
                                    'backgroundColor': '#FFBD33', #yellow
                                    'color': 'white'
                                }]
                                +
                                [{
                                    'if': {
                                        'filter_query': '{Drive} contains "Not Ready"',
                                        'column_id': 'Drive'
                                        },
                                    'backgroundColor': '#FFBD33', #yellow
                                    'color': 'white'
                                }]
                                +
                                [{
                                    'if': {
                                        'filter_query': '{Drive} contains "Running"',
                                        'column_id': 'Drive'
                                        },
                                    'backgroundColor': '#3D9970', #green
                                    'color': 'white'
                                }]
                                +
                                [{
                                    'if': {
                                        'filter_query': '{Drive} contains "Velocity mode"',
                                        'column_id': 'Drive'
                                        },
                                    'backgroundColor': '#FFBD33', #yellow
                                    'color': 'white'
                                }]
                                +
                                [{
                                'if': {
                                    'filter_query': '{{{}}} contains "Inactive"'.format(col),
                                    'column_id': col
                                },
                                'backgroundColor': '#FFBD33', #yellow
                                'color': 'white'
                                } for col in df.columns]
                            ))
                        ,
                        dcc.Interval(
                            id='interval-component',
                            interval=1*5000, # in milliseconds
                            n_intervals=0
                        )
                    ])
            ]),
        ]),
    ], className="h-100")
], color = '#1f2c56')

resultStorage_card = dbc.Card([
    dbc.CardHeader("Result Storage (Cycle Count)"), 
    dbc.CardBody([
        dbc.Row([ 
            dbc.Col([ 
                    dcc.Graph(id = 'result-storage'),
            ])
        ]),
        dbc.Row([ 
            dbc.Col([ 
                html.Div(id = 'result-storage-text', className = 'text-center')
            ])
        ]),
        dcc.Interval(id = 'gauge-interval', interval = 1*1000, n_intervals = 0)
    ])
], className="h-100", color = '#1f2c56', inverse=True)


#  BATTERY CARD ---------------------------------------------------------------------------------------------------------------


battery_card = dbc.Card([
    dbc.CardHeader("Battery Level (%)"), 
    dbc.CardBody([ 
        daq.LEDDisplay(id = 'our-LED-display', label = 'Battery %', color = '#d14952', backgroundColor = '#292F33'),
        daq.GraduatedBar(id= 'our-graduated-bar', label = 'Battery Lvl', min = 0, max = 100, color = '#d14952'),
        dcc.Interval(id = 'battery-interval', interval = 1*1000, n_intervals = 0)
    ])
], className="h-100", color = '#1f2c56', inverse=True)


#  TEMP CARD ---------------------------------------------------------------------------------------------------------------


temp_card = dbc.Card([
    dbc.CardHeader("Temperature Value (C)"), 
    dbc.CardBody([
        dbc.Row([ 
            dbc.Col([ 
                    daq.Thermometer(id = 'our-thermometer', label = 'Station 3 Temperature', labelPosition = 'top', 
                    height = 150, min = 0, max = 60, color = '#d14952'),
            ])
        ]),

        dbc.Row([ 
            dbc.Col([ 
                html.Div(id = 'temperature-text', className = 'text-left')
            ])
        ]),
        dcc.Interval(id = 'temperature-interval', interval = 1*1000, n_intervals = 0)
    ])
], className="h-100", color = '#1f2c56', inverse=True)

temp_card2 = dbc.Card([
    dbc.CardHeader("Temperature"), 
    dbc.CardBody([
        dbc.Row([ 
            dbc.Col([ 
                    dcc.Graph(id = 'temperature1'),
            ])
        ]),
        dcc.Interval(id = 'temperature1-interval', interval = 1*1000, n_intervals = 0)
    ])
], className="h-100", color = '#1f2c56', inverse=True)




#  START/STOP BUTTON LAYOUT ---------------------------------------------------------------------------------------------------------------


theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

rootLayout = dbc.Card([ 
    dbc.CardBody([ 
        daq.ToggleSwitch(id='our-power-button', 
                        size = 100, 
                        color = '#d14952', 
                        label = 'Start/Stop Button', 
                        labelPosition="bottom", 
                        className = 'dark-theme-control'),
        html.Div(id='power-button-result')
    ])
], className="h-100", color = '#1f2c56', inverse=True)

button_card = dbc.Card([
    dbc.CardHeader("Start/Stop Entry Station"), 
    dbc.CardBody([ 
        daq.DarkThemeProvider(theme=theme, children=rootLayout)
    ])
], className="h-100", color = '#1f2c56', inverse=True)

# rootLayout = dbc.Card([
#     dbc.CardHeader("Start/Stop Entry Station"), 
#     dbc.CardBody([ 
#         daq.ToggleSwitch(id='our-power-button', size = 100,color = '#d14952', labelPosition="bottom", className = 'dark-theme-control', vertical = True),
#         html.Div(id='power-button-result')
#     ])
# ], className="h-100", color = '#1f2c56', inverse=True)



#  ALERT NOTIFICATION ---------------------------------------------------------------------------------------------------------------


RS_alert = dbc.Alert("Battery running low, please charge!", color = 'danger', dismissable=True)


#  COUNTER CARD ----------------------------------------------------------------------------------------------------------------------


counter_card = dbc.Card([
    dbc.CardHeader("Machine Analytics"), 
    dbc.CardBody([ 
        dbc.Card([ 
            dbc.CardBody([ 
                html.H4(id = 'machine-status'),
                html.Small('machine status', className = 'card-text text-muted')
            ])
        ], color = '#292F33', inverse=True), 
        dbc.Row([ 
            dbc.Col([ 
                daq.LEDDisplay(id = 'no_circuit_boards', label = 'Circuit Board Count', color = '#d14952', backgroundColor = '#292F33')
            ])
        ], className = 'mt-3'),
        dbc.Row([ 
            dbc.Col([ 
                daq.LEDDisplay(id = 'performance', label = 'Performance (%)', color = '#d14952', backgroundColor = '#292F33')
            ])
        ], className = 'mt-3'),
                dbc.Row([ 
            dbc.Col([ 
                daq.LEDDisplay(id = 'availability', label = 'Availability (%)', color = '#d14952', backgroundColor = '#292F33')
            ])
        ], className = 'mt-3'),
        dcc.Interval(id = 'counter-interval', interval = 1*1000, n_intervals=0)
    ]), 
], className="h-100", color = '#1f2c56', inverse=True)


#  APP LAYOUT---------------------------------------------------------------------------------------------------------------

layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row([dbc.Col(temp_card2), dbc.Col(resultStorage_card), dbc.Col(battery_card), dbc.Col(button_card)], style={"height": "280px"}),
                    dbc.Row([dbc.Col(piechart_card), dbc.Col(bar_card)], style={"height": "300px"}, className = 'mt-5'),
                ],
                width=10,
            ),
            dbc.Col(counter_card, width=2),
        ],
        justify="center",
    ),
    dbc.Row(
        [ 
            dbc.Col(
                [ 
                    graph_card
                ],
                width=11
            )
        ],
        justify='center',
        class_name='mt-5',
        style = {'height':'300px'}
    )
    ],
    fluid=True,
    className="p-5",
    style = {'backgroundColor':'#0c1840'}
)


# CALLBACKS ---------------------------------------------------------------------------------------------------------------


# BATTERY LEVEL CALLBACKS ---------------------------------------------------------------------------------------------------------------


@app.callback(
        Output('our-LED-display', 'value'),
        Input('battery-interval', 'n_intervals')
)
def update_displays(n):

    mydb = pymysql.connect(
                host="192.168.0.207",
                user="Emmanuel_Sim",
                password= "1221",
                database = "ral_dashboard"
            )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM battery ORDER BY PID DESC LIMIT 1")
    tmp = cursor.fetchone()
    mydb.commit()
    mydb.close()

    return str(tmp[1])


@app.callback(
    Output('our-graduated-bar', 'value'),
    Input('battery-interval', 'n_intervals')
    )

def update_displays(n):
    mydb = pymysql.connect(
                host="192.168.0.207",
                user="Emmanuel_Sim",
                password= "1221",
                database = "ral_dashboard"
            )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM battery ORDER BY PID DESC LIMIT 1")
    tmp = cursor.fetchone()
    mydb.commit()
    mydb.close()

    return str(tmp[1])


#  RESULT STORAGE CALLBACKS ---------------------------------------------------------------------------------------------------

@app.callback(
    Output('result-storage', 'figure'), 
    Input('gauge-interval', 'n_intervals')
    )
def update_output(n):

    mydb = pymysql.connect(
                host="192.168.0.207",
                user="Emmanuel_Sim",
                password= "1221",
                database = "ral_dashboard"
            )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM resultstorage ORDER BY PID DESC LIMIT 1")
    rstrg = cursor.fetchone()
    mydb.commit()
    mydb.close()
    

    gauge = make_subplots(
        rows=1,
        cols=1,
        specs=[[{"type": "indicator"}]]
    )

    gauge.add_trace(
                go.Indicator(mode="gauge+number+delta", value=rstrg[1]),
                row=1,
                col=1)

    gauge.update_layout(height = 200)
    gauge.update_layout(paper_bgcolor='#1f2c56', plot_bgcolor='#1f2c56',)
    gauge.update_layout(font=dict(color='#dd1e35'))
    gauge.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return gauge
    # if value > 1800:
    #     return RS_alert, value
    # else: 
    #     print(value)
    #     return value



@app.callback(
    Output('temperature1', 'figure'), 
    Input('temperature1', 'n_intervals')
    )
def update_output(n):

    mydb = pymysql.connect(
                host="192.168.0.207",
                user="Emmanuel_Sim",
                password= "1221",
                database = "ral_dashboard"
            )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM temperature ORDER BY PID DESC LIMIT 1")
    temp = cursor.fetchone()
    mydb.commit()
    mydb.close()
    

    gauge = make_subplots(
        rows=1,
        cols=1,
        specs=[[{"type": "indicator"}]]
    )

    gauge.add_trace(
                go.Indicator(mode="gauge+number+delta", value=temp[1]),
                row=1,
                col=1)

    gauge.update_layout(height = 200)
    gauge.update_layout(paper_bgcolor='#1f2c56', plot_bgcolor='#1f2c56',)
    gauge.update_layout(font=dict(color='#dd1e35'))
    gauge.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return gauge


@app.callback(
    Output('piecharts', 'figure'), 
    Input('piechart-interval', 'n_intervals')
    )
def update_output(n):

    mydb = pymysql.connect(
                host="192.168.0.207",
                user="Emmanuel_Sim",
                password= "1221",
                database = "ral_dashboard"
            )
    cursor = mydb.cursor()
    cursor2 = mydb.cursor()

    cursor.execute("SELECT * FROM runtime ORDER BY PID DESC LIMIT 1")
    runtime = cursor.fetchone()

    cursor2.execute("SELECT * FROM actualoutput ORDER BY PID DESC LIMIT 1")
    actualoutput = cursor2.fetchone()


    mydb.commit()
    mydb.close()

    current = datetime.now()

    diff = current - const

    timePassed = diff.total_seconds() - diff.days*86400

    # print(timePassed)  ----  TME PASSED SINCE 8:00AM (SECONDS) // A.T.

    totalProjected = timePassed/45   


    night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                'rgb(36, 55, 57)', 'rgb(6, 4, 4)']
    sunflowers_colors = ['rgb(177, 127, 38)', 'rgb(205, 152, 36)', 'rgb(99, 79, 37)',
                        'rgb(129, 180, 179)', 'rgb(124, 103, 37)']
    irises_colors = ['rgb(33, 75, 99)', 'rgb(79, 129, 102)', 'rgb(151, 179, 100)',
                    'rgb(175, 49, 35)', 'rgb(36, 73, 147)']
    cafe_colors =  ['rgb(146, 123, 21)', 'rgb(177, 180, 34)', 'rgb(206, 206, 40)',
                    'rgb(175, 51, 21)', 'rgb(35, 36, 21)']


    RunTime = runtime[1]/(9*60*60)

    Performace = actualoutput[1]/totalProjected


    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
    # Define pie charts
    fig.add_trace(go.Pie(values=[RunTime*100, (100-RunTime)], name='Run Time',
                        marker_colors=night_colors), 1, 1)
    fig.add_trace(go.Pie(values=[Performace*100, (100-Performace)], name='Performance',
                        marker_colors=sunflowers_colors), 1, 2)
    fig.add_trace(go.Pie(values=[100], name='Quality',
                        marker_colors=irises_colors), 1, 3)

    # Tune layout and hover infos
    fig.update_traces(hoverinfo='label+percent+value+name', hole = 0.7, rotation = 45, textinfo='label+value', textfont=dict(color = 'white'))
    fig.update_layout(height = 250)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    fig.update(layout_showlegend=False)
    fig.update_layout(paper_bgcolor='#1f2c56', plot_bgcolor='#1f2c56', 
                        title = {'text':'OEE'}, 
                        titlefont={'color': 'white', 'size': 15}, hovermode='closest')

    fig = go.Figure(fig)

    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig



# TEMPERATURE CALLBACKS ---------------------------------------------------------------------------------------------



@app.callback(
    Output('barchart', 'figure'), 
    Input('barchart-interval', 'n_intervals')
    )
def update_output(n):

    mydb = pymysql.connect(
                host="192.168.0.207",
                user="Emmanuel_Sim",
                password= "1221",
                database = "ral_dashboard"
            )
    cursor = mydb.cursor()
    data = {
        "Temperature":[],
        "Time":[]
    }

    cursor.execute("SELECT * FROM temperature ORDER BY PID DESC LIMIT 5")
    tmp = cursor.fetchall()
    mydb.commit()

    for i in range(len(tmp)):
        data['Temperature'].append(tmp[i][1])
        data['Time'].append(tmp[i][2])

    df1 = pd.DataFrame(data)
    df1['Time'] = pd.to_datetime(df1['Time'],format).apply(lambda x: x.time())
    df1=df1.iloc[::-1]

    mydb.close()

    fig = px.bar(df1, x='Time', y='Temperature')
    fig.update_layout(height = 250)
    fig.update_layout(paper_bgcolor='#1f2c56', plot_bgcolor='#1f2c56')
    fig.update_layout(font=dict(color='#ffffff'))
    fig.update_traces(marker_color='#d14952')
    fig.update_xaxes(title = 'Time (s)')
    fig.update_yaxes(title = 'Temperature (C)')

    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig




# #  BUTTON CALLBACKS ---------------------------------------------------------------------------------------------


# @app.callback(
#     Output('power-button-result', 'children'),
#     Input('our-power-button', 'on')
# )
# def update_output(on):
#     if temp==on:
#         key.set_value(True,varianttype=None)
#         state=key.get_value()
#         print(state)
#     else:
#         key.set_value(False,varianttype=None)
#         state=key.get_value()
#         print(state)
#     return f'The button is {on}.'


# #  COUNTER CALLBACKS ---------------------------------------------------------------------------------------------


@app.callback(
    Output('no_circuit_boards', 'value'),
    Input('counter-interval', 'n_intervals')
)
def update_counter(n):

    mydb = pymysql.connect(
        host="192.168.0.207",
        user="Emmanuel_Sim",
        password= "1221",
        database = "ral_dashboard"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM actualoutput ORDER BY PID DESC LIMIT 1")
    count = cursor.fetchone()
    mydb.commit()
    
    return count[1]


@app.callback(
    Output('machine-status', 'children'),
    Input('counter-interval', 'n_intervals')
)
def update_div(n):

    mydb = pymysql.connect(
        host="192.168.0.207",
        user="Emmanuel_Sim",
        password= "1221",
        database = "ral_dashboard"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM machine_status ORDER BY PID DESC LIMIT 1")
    mstatus = cursor.fetchone()
    mydb.commit()
    mydb.close()
    if mstatus[1] == True:
        return [html.Span('Simulation', style={'color':'#04d9ff'})]
    elif mstatus[1] == False:
        return [html.Span('Production', style={'color':'#18c930'})]




@app.callback(
    Output('performance', 'value'),
    Input('counter-interval', 'n_intervals')
)
def update_performance(n):  
    mydb = pymysql.connect(
        host="192.168.0.207",
        user="Emmanuel_Sim",
        password= "1221",
        database = "ral_dashboard"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM actualoutput ORDER BY PID DESC LIMIT 1")
    tmp = cursor.fetchone()
    print(tmp[1])
    mydb.commit()

    current = datetime.now()

    diff = current - const

    timePassed = diff.total_seconds() - diff.days*86400

    # print(timePassed)  ----  TME PASSED SINCE 8:00AM (SECONDS) // A.T.

    totalProjected = timePassed/45      

    mydb.close()
    print(tmp[1]/int(totalProjected),3)
    return round((tmp[1]/int(totalProjected))*100, 1)




@app.callback(
    Output('availability', 'value'),
    Input('counter-interval', 'n_intervals')
)
def update_performance(n):  
    mydb2 = pymysql.connect(
        host="192.168.0.207",
        user="Emmanuel_Sim",
        password= "1221",
        database = "ral_dashboard"
    )
    cursor2 = mydb2.cursor()
    cursor2.execute("SELECT * FROM actualoutput ORDER BY PID DESC LIMIT 1")
    tmp = cursor2.fetchone()
    mydb2.commit()
    mydb2.close()

    return round((tmp[1]/(9*60*60))*100,3)


@app.callback(Output('table', 'data'),
            Input('interval-component', 'n_intervals'))    

def update_graph(n):
    data={
    "Station":[],
    "Doorlocked_f":[],
    "Doorlocked_b":[],
    "fts_f":[],
    "fts_b":[],
    "Drive":[],
    "Rfid":[],
    "Estop":[],
    "Timestamp":[]
}   
    cursor=db.cursor()
    cursor.execute(("SELECT * FROM entry ORDER BY PID DESC LIMIT 1"))
    testresult=cursor.fetchall()
    db.commit()
    try:
        for i in range(len(testresult)):
                    data['Station'].append("Entry")
                    data['Doorlocked_f'].append(testresult[i][1])
                    data['Doorlocked_b'].append(testresult[i][1])
                    data['fts_f'].append(testresult[i][2])
                    data['fts_b'].append(testresult[i][2])
                    data['Drive'].append(testresult[i][3])
                    data['Rfid'].append(testresult[i][4])
                    data['Estop'].append(testresult[i][5])
                    data['Timestamp'].append(testresult[i][6])
    except Exception as error:
        print("Database is Null")
        print(error)
    cursor.execute(("SELECT * FROM dispensing ORDER BY PID DESC LIMIT 1"))
    testresult=cursor.fetchall()
    db.commit()
    try:
            for i in range(len(testresult)):
                        data['Station'].append("Dispensing")
                        data['Doorlocked_f'].append(testresult[i][1])
                        data['Doorlocked_b'].append(testresult[i][2])
                        data['fts_f'].append(testresult[i][3])
                        data['fts_b'].append(testresult[i][4])
                        data['Drive'].append(testresult[i][5])
                        data['Rfid'].append(testresult[i][6])
                        data['Estop'].append(testresult[i][7])
                        data['Timestamp'].append(testresult[i][8])
                    
    except Exception as error:
        print("Database is Null")
        print(error)
    cursor=db.cursor()
    print("Connected")
    cursor.execute(("SELECT * FROM pickandplace ORDER BY PID DESC LIMIT 1"))
    testresult=cursor.fetchall()
    db.commit()
    try:
            for i in range(len(testresult)):
                        data['Station'].append("Pick and place")
                        data['Doorlocked_f'].append(testresult[i][1])
                        data['Doorlocked_b'].append(testresult[i][2])
                        data['fts_f'].append(testresult[i][3])
                        data['fts_b'].append(testresult[i][4])
                        data['Drive'].append(testresult[i][5])
                        data['Rfid'].append(testresult[i][6])
                        data['Estop'].append(testresult[i][7])
                        data['Timestamp'].append(testresult[i][8])
                    
    except Exception as error:
        print("Database is Null")
        print(error)
    cursor.execute(("SELECT * FROM tightening ORDER BY PID DESC LIMIT 1"))
    testresult=cursor.fetchall()
    db.commit()
    try:
            for i in range(len(testresult)):
                        data['Station'].append("Tightening")
                        data['Doorlocked_f'].append(testresult[i][1])
                        data['Doorlocked_b'].append(testresult[i][2])
                        data['fts_f'].append(testresult[i][3])
                        data['fts_b'].append(testresult[i][4])
                        data['Drive'].append(testresult[i][5])
                        data['Rfid'].append(testresult[i][6])
                        data['Estop'].append(testresult[i][7])
                        data['Timestamp'].append(testresult[i][8])
                    
    except Exception as error:
        print("Database is Null")
        print(error)
    cursor.execute(("SELECT * FROM exit_station ORDER BY PID DESC LIMIT 1"))
    testresult=cursor.fetchall()
    db.commit()
    try:
        for i in range(len(testresult)):
                    data['Station'].append("Exit")
                    data['Doorlocked_f'].append(testresult[i][1])
                    data['Doorlocked_b'].append(testresult[i][1])
                    data['fts_f'].append(testresult[i][2])
                    data['fts_b'].append(testresult[i][2])
                    data['Drive'].append(testresult[i][3])
                    data['Rfid'].append(testresult[i][4])
                    data['Estop'].append(testresult[i][5])
                    data['Timestamp'].append(testresult[i][6])
    except Exception as error:
        print("Database is Null")
        print(error)
    global df
    df = pd.DataFrame(data)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'],format).apply(lambda x: x.time()) #remove date, keep time only
    df=df.iloc[::-1] #orders time from oldest to latest
    df.loc[df['Doorlocked_f'] == 2, 'Doorlocked_f'] = "Closed" #changes value of doorstate to strings
    df.loc[df['Doorlocked_f'] == 1, 'Doorlocked_f'] = "Open"
    df.loc[df['Doorlocked_b'] == 2, 'Doorlocked_b'] = "Closed"
    df.loc[df['Doorlocked_b'] == 1, 'Doorlocked_b'] = "Open"
    df.loc[df['Drive'] == 'Ab', 'Drive'] = "Initializing"
    df.loc[df['Drive'] == 'AF', 'Drive'] = "Running"
    df.loc[df['Drive'] == 'Fatal', 'Drive'] = "Error"
    df.loc[df['Rfid'] == 1, 'Rfid'] = "Active"
    df.loc[df['Rfid'] == 0, 'Rfid'] = "Error"
    df.loc[df['Estop'] == 1, 'Estop'] = "Active"
    df.loc[df['Estop'] == 0, 'Estop'] = "Error"
    df["Door"] = df['Doorlocked_f'].astype(str) +"\n"+ df["Doorlocked_b"]
    df["Fts"] = df['fts_f'] +"\n"+ df["fts_b"]
    df=df.drop(columns=['Doorlocked_f','Doorlocked_b'])
    df=df.drop(columns=['fts_f','fts_b'])
    df.loc[df['Door'] == "Open\nClosed", 'Door'] = "Front (Unlocked)\nBack (Locked)"
    df.loc[df['Door'] == "Open\nOpen", 'Door']  = "Front (Locked)\nBack  (Unlocked)"
    df.loc[df['Door'] == "Closed\nClosed", 'Door'] = "Front (Locked)\nBack (Locked)"
    df.loc[df['Door'] == "Closed\nOpen", 'Door'] = "Front (Locked)\nBack (Unlocked)"
    df.loc[df['Fts'] == "Active\nActive", 'Fts'] = "Front (Active)\nBack (Active)"
    df.loc[df['Fts'] == "Active\nInactive", 'Fts'] = "Front (Active)\nBack (Inactive)"
    df.loc[df['Fts'] == "Inactive\nActive", 'Fts'] = "Front (Inactive)\nBack (Active)"
    df.loc[df['Fts'] == "Inactive\nInactive", 'Fts'] = "Front (Inactive)\nBack (Inactive)"
    df.loc[df['Fts'] == "Idle\nIdle", 'Fts'] = "Front (Idle)\nBack (Idle)"
    df.loc[df['Fts'] == "Closed\nOpen", 'Fts'] = "Front (Locked)\nBack (Unlocked)"
    df['Door'] = np.where((df['Door'] == "Front (Locked)\nBack (Locked)") & (df['Station'] == 'Entry'), "Front (Locked)", df['Door'])
    df['Door'] = np.where((df['Door'] == "Front (Unlocked)\nBack (Unlocked)") & (df['Station'] == 'Entry'), "Front (Unlocked)", df['Door'])
    df['Door'] = np.where((df['Door'] == "Front (Locked)\nBack (Locked)") & (df['Station'] == 'Exit'), "Front (Locked)", df['Door'])
    df['Door'] = np.where((df['Door'] == "Front (Unlocked)\nBack (Unlocked)") & (df['Station'] == 'Exit'), "Front (Unlocked)", df['Door'])
    df=df[['Station','Door','Fts','Drive','Rfid','Estop','Timestamp']]
    df = df.sort_index(ascending=True)
    print(df)
    data=df.to_dict('records')
    return data
# if __name__ == '__main__':
#     app.run_server(debug=False)


