from dash_iconify import DashIconify as di
from dash import html,dash_table
from apps import commonmodule as cm
import pandas
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
        dbc.Card(
            [
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
                        dbc.Label("Filter by: ",style={"padding-right":"1em"}),
                        dbc.Select(
                                id="filter-select",
                                options=[
                                    {"label": "Member Type", "value": "1"},
                                    {"label": "Year Standing", "value": "2"},
                                    {"label": "App Batch", "value": "3"},
                                    {"label": "Accountabilities", "value": "4","disabled":True},
                                ],
                            ),
                        dbc.Input(type="text", placeholder="Filter",id="prof-filter"),
                   
            ],
            width=6,
        class_name='flex part-3 center-align'),
    ],
    className="g-7"
,style={"width":"100%"}),
],class_name='flex '),

dbc.Container(["No Members to Display"],id="mem-table",class_name='table-wrapper')
            ],
            class_name="custom-card"
        )
    ],className='body')
])
@app.callback(
    Output('mem-table','children'),
    Input('url','pathname')
)
def mem_pop(pathname):
    if pathname=="/members":
        sql="""	SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name,birthdate,membership_type,app_batch,year_standing,degree_program,other_org_affiliation,email,present_address
            FROM 
            person LEFT JOIN upciem_member 
            ON person.valid_id=upciem_member.valid_id LEFT JOIN affiliation 
            ON person.valid_id=affiliation.valid_id 
            WHERE upciem_member_delete is NULL or upciem_member_delete=False
            """
        values=[]
        cols=["Name","Birthday","Membership","App Batch","Year Standing","Degree Program","Other Orgs","Email","Present Address"]
        df = db.querydatafromdatabase(sql, values, cols)
        print(df.shape[0])
        if df.shape[0]:
            print(df.columns)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
            hover=True, size='sm')
            return table
        return "No Members to Display"
    raise PreventUpdate