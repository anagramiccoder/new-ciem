import webbrowser
from dash_iconify import DashIconify as di
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
import dash_bootstrap_components as dbc
# Importing your app definition from app.py so we can use it
from app import app
from apps import commonmodule as cm
from pages import home,alumni,changepassword, generatereport,managers,members,reaffiliate,updatealum,updatemember,login,updatemem
app.layout = html.Div([dcc.Location(id='url',refresh=False),
    html.Div(id='page-content')])

@app.callback(
    [
        
        Output('page-content', 'children'),
        Output('url','pathname')
    ],
    [
        Input('url', 'pathname'),
    ],
)
def displaypage (pathname):
    data={'isAuthenticated':True}
    print('current data in display->', data)
    ctx = dash.callback_context
    if ctx.triggered:
        eventids = ctx.triggered
        for eventidmore in eventids:
            eventid=eventidmore['prop_id'].split('.')[0]
            if eventid == 'url':
                if data['isAuthenticated']:
                    if pathname=='/logout':
                        return [login.layout],'/login'
                    if pathname == '/' or pathname == '/home':
                        print("home")
                        pathname='/home'
                        returnlayout = home.layout
                    elif pathname=="/change-password":
                        returnlayout=changepassword.layout
                    # elif pathname=="/edit-profile":
                    #     returnlayout=reaffiliate.layout
                    elif pathname=="/view-reports":
                        returnlayout=generatereport.layout
                    elif pathname=="/managers":
                        pathname="/managers"
                        returnlayout=managers.layout
                    elif pathname=="/members":
                        returnlayout=members.layout
                    elif pathname=="/reaffiliate":
                        returnlayout=reaffiliate.layout
                    elif pathname=="/update-alumni":
                        returnlayout=updatealum.layout
                    elif pathname=="/update-member":
                        returnlayout=updatemember.layout
                    elif pathname=="/alumni":
                        returnlayout=alumni.layout
                    elif pathname=='/update-member-modify':
                        returnlayout=updatemem.layout
                    else:
                        returnlayout = 'error404'
                    return returnlayout,pathname
                else:
                    return [login.layout],'/login'
            elif data['isAuthenticated'] and pathname=='/login':
                    return dash.no_update,'/home'
            elif not data['isAuthenticated']:
                    return [login.layout],'/login'
            else:
                PreventUpdate
    else:
        raise PreventUpdate
if __name__ == '__main__': 
    app.run_server(debug=True)