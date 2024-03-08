from dash_iconify import DashIconify as di
from dash import html
from apps import commonmodule as cm
from apps import dbconnect as db
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
        html.Div([
            dbc.Card([
                dbc.CardHeader([html.H3("Hello,"), html.H3("User",id='session-user')],class_name='flex'),
                dbc.CardBody([
                    dbc.Container(
                        [
                            dbc.Card([dbc.CardHeader("Members"),dbc.CardBody("Total here",id='total-mem-home'),dbc.CardFooter(dbc.NavLink("Check Members>",href="/members"))]),
                            dbc.Card([dbc.CardHeader("Alumni"),dbc.CardBody("Total here",id='total-alum-home'),dbc.CardFooter(dbc.NavLink("Check Alumni>",href="/alumni"))]),
                            dbc.Card([dbc.CardHeader("Members"),dbc.CardBody("Total here",id='home-user'),dbc.CardFooter(dbc.NavLink("View Profile>"))]),
                            
                        ],class_name='flex homeshow'
                    )
                ])
            ]),
            dbc.Card([
                dbc.CardBody([
                    
                html.H2("One Circle, One Family",
                    style={
                    "text-align": "center",
                    "font-family": "Tahoma",
                    "font-size":"3rem",
                    "margin-top": "0",
                    "margin-bottom": "0",
                    "color": "#273250",
                    "font-weight":"bolder"
                    }
                    ),
            html.H2("Expanding the Circle Since 1976",
                    style={
                    "text-align": "center",
                    "font-family": "Tahoma",
                    "font-size":"1.5em",
                    "margin-bottom": "0.5em",
                    "margin-top": "0",
                    "color": "#273250",
                    "font-weight":"bold"}
                    ),
            dbc.Container([
            dbc.Carousel(
                    items=[
                        {"key": "1", "src": "/static/ciem1.jpg"},
                        {"key": "2", "src": "/static/ciem3.jpg"},
                        {"key": "3", "src": "/static/ciem4.jpg"},
                    ],
                    controls=False,
                    indicators=False,
                    interval=1000,
                    ride="carousel",
                    style={'aspect-ratio':'16/9','height':'450px','overflow-y':'hidden'},
                ),
            dbc.Container([
                html.H2("About CIEM",
                    style={
                    "text-align": "left",
                    "font-family": "Tahoma",
                    "font-size":"1.5em",
                    "margin-bottom": "0.3em",
                    "margin-top": "0.5em",
                    "color": "#273250",
                    "font-weight":"bold"}
                    ),
            html.H4("The University of the Philippines Circle of Industrial Engineering Majors (UP CIEM) was established on November 23, 1976 by a group of students from the Department of Industrial Engineering and Operations Research, College of Engineering at the University of the Philippines, Diliman. Over the years, UP CIEM has grown from a fledging organization to a force to be reckoned with, not only in academics but in sports, social activities, and leadership as well. The business of UP CIEM never falls short of the foundations of Industrial Engineering – effectiveness, efficiency, and productivity. UP CIEM is a duly recognized college-wide, socio-academic organization. UP CIEM consistently makes its mark through rendering service to the college, the university, and the country by upholding its core values: academic excellence, leadership in service, and social relevance through numerous projects that cater to the needs of Industrial Engineering students. More than being an organization, UP CIEM continues to be the family of camaraderie and trust for the IE student body and the sanctuary of excellent Industrial Engineers for the nation’s future.",
                    style={
                    "font-family": "Arial",
                    "font-weight":"normal",
                    "text-align":"justify",
                    "margin":"0"}
                    ),]      
            ),
            ], class_name='flex')
            ])
            ,
            dbc.CardFooter(
                [
                    dbc.Button([di(icon='mingcute:facebook-line',inline=True),dbc.Label("Facebook Page")],href="https://www.facebook.com/upciem",external_link=True),
                    dbc.Button([di(icon='bi:instagram',inline=True),dbc.Label("Instagram")],href="https://www.instagram.com/upciem/",external_link=True),
                    dbc.Button([di(icon='iconoir:twitter',inline=True),dbc.Label("Twitter")],href="https://twitter.com/upciem",external_link=True),
                    dbc.Button([di(icon='lucide:linkedin',inline=True),dbc.Label("LinkedIn")],href="https://ph.linkedin.com/company/upciem1976",external_link=True), 
                ]
                ,style={'display':'flex','justify-content':'space-evenly'}
            )
            ])
            ], 
                className="body"),
    ],className='flex body-container')
])
@app.callback(
    [
        Output('total-mem-home','children'),
        Output('total-alum-home','children'),
        Output('home-user','children'),
    ],
    Input('url','pathname')
)
def total(pathname):
    #childrens to be called back
    memchildren=[]
    alumchildren=[]
    profchildren=[]
    if pathname=="/home":
        #This is for the members
        sql="SELECT COUNT(*) FROM upciem_member WHERE upciem_member_delete is NULL or upciem_member_delete=False"
        cols=['count']
        df=db.querydatafromdatabase(sql,[],cols)
        #will always return some count but can be 0
        memchildren+=[html.H1(df['count'][0])]
        memchildren+=[html.P("Total Members in the Database")]
        #info for the alumni
        sql="SELECT COUNT(*) FROM alumni"
        cols=['count']
        df=db.querydatafromdatabase(sql,[],cols)
        alumchildren+=[html.H1(df['count'][0])]
        alumchildren+=[html.P("Total Alumni in the Database")]
        return memchildren,alumchildren,profchildren
    raise PreventUpdate