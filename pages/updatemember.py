from dash_iconify import DashIconify as di
from dash import html
from apps import commonmodule as cm
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
import dash_bootstrap_components as dbc
from app import app
layout=html.Div([
    
        cm.navigation,
        cm.top,
    html.Div([
        dbc.Container([dbc.Label("Search Name"),dbc.Input(id='alum-search',type='text')])
    ],className='flex container')
])