import dash
from dash import dcc 
from dash import html
import logging
app = dash.Dash(__name__, external_stylesheets = ['assets/bootstrap.css','assets/custom.css'])
app.config.suppress_callback_exceptions = True

app.css.config.serve_locally = True

app.scripts.config_serve_locally = True

app.title = 'CIEM BLUEPrint'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)