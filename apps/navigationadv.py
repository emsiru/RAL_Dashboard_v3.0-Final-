import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components import Container
from app import app


# bootstrap uses 12 col system
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row([
                dbc.Col([
                    html.Img(src=app.get_asset_url('logo2.png'), height="60px"),
                    dbc.NavbarBrand('Robotic-Assembly Line Dashboard', style={'color': 'white', 'fontSize': 20, 'font':'sans-serif'}, className = 'ms-4')
                ], width = {'size':'auto'})
            ]),
                dbc.Row([   
                    dbc.Col([
                        dbc.Nav([
                            dbc.NavItem(dbc.NavLink('Home', href = '/', style={'color':'white'})),
                            # dbc.NavItem(dbc.NavLink('Drill Torque Gauge', href = '/apps/gauge')),
                            dbc.NavItem(dbc.NavLink('Live-Graph', href = '/apps/graph', style={'color':'white'})),
                            # dbc.NavItem(dbc.DropdownMenu(
                            #     children = [
                            #         dbc.DropdownMenuItem('More pages etc.', header = True),
                            #         dbc.DropdownMenuItem('Extra component', href = '/extras')
                            #     ],
                            #         nav = True,
                            #         in_navbar = True,
                            #         label = 'More'
                            #                             ))
                                ],
                                    navbar=True
                                )
                            ], width={'size':'auto'})
                        ], align='center')
            ],
        fluid = True
        )
,color = '#1f2c56')