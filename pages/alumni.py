from dash_iconify import DashIconify as di
from dash import html
from apps import commonmodule as cm
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
import dash_bootstrap_components as dbc
from apps import dbconnect as db
from app import app
layout=html.Div([
    
        cm.navigation,
        cm.top,
    html.Div([
        dbc.Container([dbc.Row(
    [
        dbc.Col(
            [
                dbc.FormFloating(
                    [
                        dbc.Input(type="text", placeholder="Enter Name",id="alum-name"),
                        dbc.Label("Search Name"),
                    ]
                )
            ],
            width=6,
        ),
        dbc.Col(
            [
                dbc.FormFloating(
                    [
                        dbc.Input(type="text", placeholder="Profession",id="prof-filter"),
                        dbc.Label("Filter by Profession"),
                    ]
                )
            ],
            width=6,
        ),
    ],
    className="g-7"
,style={"width":"100%"}),
],class_name='flex '),

dbc.Container(["No Alumni to Display"],id="alum-table",class_name='table-wrapper')
    ],className='body')
])
@app.callback(
    Output("alum-table","children"),
    [Input("url","pathname"),Input("prof-filter","value"),Input("alum-name","value")]

)
def show_alumni(pathname,filter,name):
    if pathname=="/alumni":
        sql="""SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name,birthdate, specialization
            FROM alumni left join person on alumni.valid_id=person.valid_id WHERE True
            """
        values=[]
        cols=["Full Name","Birthdate","Specialization"]
        if name:
            sql+="""AND CONCAT(first_name||' '||middle_name||' '||last_name||' '||suffix) ILIKE %s"""
            values+={f"%{name}%"}
        if filter:
            sql+="AND specialization ILIKE %s"
            values+={f"%{filter}%"}
        df = db.querydatafromdatabase(sql, values, cols)
        df=db.querydatafromdatabase(sql,values,cols)
        if df.shape[0]: 
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
            hover=True, size='sm')
            return table
        return "No Members to Display"
    raise PreventUpdate