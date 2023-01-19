from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_auth

# Connect to main app.py file
from app import app
from app import server

from apps import navigationadv, graph1, dboard_layout_DT

# url = "opc.tcp://192.168.0.30:4840"
# client = Client(url)


# auth = dash_auth.BasicAuth(
#     app, {'admin':'1'}
# )

app.layout = html.Div([
    html.Div(navigationadv.navbar),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),   
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/graph':
        return graph1.layout
    else:
        return dboard_layout_DT.layout


if __name__ == '__main__':
    app.run_server(debug=False, port = 3000)

