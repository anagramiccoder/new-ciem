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
        dbc.Card([
            dbc.CardBody(
                [
                html.Div([
                    dbc.CardHeader(html.H1("LOGIN")),
                        dbc.Input(id='uname', type='text', className='input', placeholder='Username'),
                        dbc.Input(type='password', id='pword', className='input', placeholder='Password'),
                        html.H4(id='errormessage', className='error'),
                        dbc.Button('Log In', id='submit-val', className='loginbutton', n_clicks=0),

                ],className='half left'),
                html.Div([
                ],className='half')
                ],
            ),
        ], class_name='flex small')
    ],className='FullScreen')
