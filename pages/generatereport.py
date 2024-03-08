from dash_iconify import DashIconify as di
from dash import html
import math
import dash
import pandas as pd
from apps import commonmodule as cm
from apps import dbconnect as db
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from datetime import datetime
import dash_bootstrap_components as dbc
from app import app
layout=html.Div([
        dcc.Store(id='pref-mem',data=[]),
        cm.navigation,
        cm.top,
    html.Div([
        dbc.Card([
            dbc.CardHeader(html.H4("Members")),
            dbc.CardBody([
                dbc.Container([
                    dbc.Card([dbc.CardHeader("New and Reaffiliated Members"),dbc.CardBody("c1",id='new-reaff')]),
                    dbc.Card([dbc.CardHeader("Active and Inactive Members"),dbc.CardBody("c2",id='act-inact')]),
                    dbc.Card([dbc.CardHeader("New and Reaffiliated Members"),dbc.CardBody("c3",id='alum-mem')]),
                ], class_name='percentage'),
                dbc.Container([
                    dbc.Tabs(
                        [
                            dbc.Tab(dbc.Container(id='new-table',class_name='sm-table-wrapper'),label="New Members",),
                            dbc.Tab(dbc.Container(id='reaff-table',class_name='sm-table-wrapper'),label="Reaffiliated Members",),
                            dbc.Tab(dbc.Container(id='act-table',class_name='sm-table-wrapper'),label="Active Members",),
                            dbc.Tab(dbc.Container(id='inact-table',class_name='sm-table-wrapper'),label="Inactive Members",),
                        ]
                    )
                ])
            ]),
            
        ]),
        dbc.Card([
            dbc.CardHeader(html.H4("Headships")),
            dbc.CardBody([
                dbc.Container([
                    dbc.Card([dbc.CardHeader("Academic Affairs"),dbc.CardBody(["here is body"],id='af')]),
                    dbc.Card([dbc.CardHeader("External Affairs"),dbc.CardBody(["here is body"],id='ef')]),
                    dbc.Card([dbc.CardHeader("Finance"),dbc.CardBody(["here is body"],id='fi')]),
                    dbc.Card([dbc.CardHeader("Internal Affairs"),dbc.CardBody(["here is body"],id='if')]),
                    dbc.Card([dbc.CardHeader("Membership and Recruitment"),dbc.CardBody(["here is body"],id='mr')]),
                    dbc.Card([dbc.CardHeader("Publications and Records"),dbc.CardBody(["here is body"],id='pr')]),
                    dbc.Card([dbc.CardHeader("No Committee"),dbc.CardBody(["here is body"],id='no')]),
                ], class_name='flex headship-cards'),
                dbc.Container([
                    dbc.Tabs(
                        [
                            dbc.Tab(dbc.Container(id='all-table',class_name='sm-table-wrapper'),label="All Active",),
                            dbc.Tab(dbc.Container(id='af-table',class_name='sm-table-wrapper'),label="Academic Affairs",),
                            dbc.Tab(dbc.Container(id='ef-table',class_name='sm-table-wrapper'),label="External Affairs",),
                            dbc.Tab(dbc.Container(id='fi-table',class_name='sm-table-wrapper'),label="Finance",),
                            dbc.Tab(dbc.Container(id='if-table',class_name='sm-table-wrapper'),label="Internal Affairs",),
                            dbc.Tab(dbc.Container(id='mr-table',class_name='sm-table-wrapper'),label="Membership and Recruitment",),
                            dbc.Tab(dbc.Container(id='pr-table',class_name='sm-table-wrapper'),label="Publication and Records",),
                            dbc.Tab(dbc.Container(id='no-table',class_name='sm-table-wrapper'),label="No Committee",),
                        ]
                    )
                ])
            ]),
            
        ]),
        dbc.Card([
            dbc.CardHeader(html.H4("Member List")),
            dbc.CardBody([
                dbc.Tabs(
                    [
                        dbc.Tab([],id='com-tab',label='By Committee'),
                        dbc.Tab([],id='year-tab',label='By Year Level'),
                        dbc.Tab([],id='batch-tab',label='By App Batch'),
                        dbc.Tab([],id='acc-tab',label='By Accountabilities',disabled=True),
                    ]
                )
            ])
        ]),
        dbc.Card([
            dbc.CardHeader(html.H4("Committee Preferences")),
            dbc.CardBody([
                dbc.Container([html.H5("**This is just based on the preferences for now, please click 'Update Committee' to update the committee of each,"),dbc.Button("Update Committee")],class_name='flex in-between'),
                dbc.Container(id='pref-table')
            ])
        ]),
        dbc.Card([
            dbc.CardHeader(html.H4("14 White Stripes")),
            dbc.CardBody([
                dbc.Container(id='ws',class_name='ws')
            ])
        ])
    ],className='body')
])
@app.callback(
    [
        Output('new-reaff','children'),
        Output('act-inact','children'),
        Output('alum-mem','children'),
        Output('new-table','children'),
        Output('reaff-table','children'),
        Output('act-table','children'),
        Output('inact-table','children'),
        Output('af','children'),
        Output('ef','children'),
        Output('fi','children'),
        Output('if','children'),
        Output('mr','children'),
        Output('pr','children'),
        Output('no','children'),
        Output('af-table','children'),
        Output('ef-table','children'),
        Output('fi-table','children'),
        Output('if-table','children'),
        Output('mr-table','children'),
        Output('pr-table','children'),
        Output('no-table','children'),
        Output('all-table','children'),
        Output('com-tab','children'),
        Output('year-tab','children'),
        Output('batch-tab','children'),
        Output('ws','children')
    ],
    
    Input('url','pathname'),
)
def generate(pathname):
    new_reaff_children=[]
    act_inact_children=[]
    if pathname=="/view-reports":
        #get all members all active, inactive, new, reaffilated
        sql="""
            SELECT gwa,is_new,active_status, CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name,birthdate,membership_type,app_batch,year_standing,degree_program,other_org_affiliation,email,present_address,committee_id
            FROM 
            person LEFT JOIN upciem_member 
            ON person.valid_id=upciem_member.valid_id JOIN affiliation 
            ON person.valid_id=affiliation.valid_id 
            WHERE upciem_member_delete is NULL or upciem_member_delete=False
        """
        #JOIN only on affilation since we filter those acc that has no affiliation, can change if required
        cols=['gwa','new','active','Full Name',"Birthday","Membership","App Batch","Year Standing","Degree Program","Other Orgs","Email","Present Address",'committee_id']
        #full dataframe for now
        df=db.querydatafromdatabase(sql,[],cols)
        if not df.shape[0]:#just for full proofing of an empty row
            raise PreventUpdate #if it is indeed empty do nothing
        #else will proceed here
        #start of filtering
        #filtering of active members now
        active_mem=df[df['active']=='Active']#will only filter active members
        #using active members will now filter new and reaffilated members
        new_mem=active_mem[active_mem['new']==True]
        reaff_mem=active_mem[active_mem['new']==False]
        #create a donut graph for the counts
        new_reaff_fig=px.pie(names=['New Members','Reaffiliated Members'],values=[new_mem.shape[0],reaff_mem.shape[0]],hole=0.5)
        new_reaff_fig.update_traces(marker=dict(colors=['#273250','#3f66bd']))
        new_reaff_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),  # Adjusted margins
        paper_bgcolor='rgba(0,0,0,0)'
    )
        new_reaff_fig.update_layout(
            legend=dict(
                font=dict(color="white"),
                orientation="v",  # Set horizontal orientation
                yanchor="bottom",  # Anchor to the bottom
                y=1.02,  # Position slightly above the plot (adjust as needed)
                xanchor="center",  # Center align
                x=0.5
            ),
        )
        new_reaff_children+=[
            dcc.Graph(figure=new_reaff_fig,style={'width': '100%', 'height': '100%'})
        ]
        #We go for the active and inactive status now, since we have active_mem df already, we only need the inactive mem df
        inactive_mem=df[df['active']=='Inactive']
        #we create another donut for acgtive-inactive
        act_inact_fig=px.pie(names=['Active Members','Inactive Members'],values=[active_mem.shape[0],inactive_mem.shape[0]],hole=0.5,)
        act_inact_fig.update_traces(marker=dict(colors=['#e15789','#3f66bd']))
        act_inact_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),  # Adjusted margins
        paper_bgcolor='rgba(0,0,0,0)'
    )
        act_inact_fig.update_layout(
            legend=dict(
                
                font=dict(color="white"),
                orientation="v",  # Set horizontal orientation
                yanchor="bottom",  # Anchor to the bottom
                y=1.02,  # Position slightly above the plot (adjust as needed)
                xanchor="center",  # Center align
                x=0.5
            ),
        )
        act_inact_children+=[
            dcc.Graph(figure=act_inact_fig,style={'width': '100%', 'height': '100%'})
        ]

        #This is for the tables
        #before adding tables modify dataframes to remove the 'new' and 'active' columns
        active_mem=active_mem.drop(columns=['new','active','committee_id','gwa'])
        inactive_mem=inactive_mem.drop(columns=['new','active','committee_id','gwa'])
        new_mem=new_mem.drop(columns=['new','active','committee_id','gwa'])
        reaff_mem=reaff_mem.drop(columns=['new','active','committee_id','gwa'])
        #now we create tables
        act_table=dbc.Table.from_dataframe(active_mem, striped=True, bordered=True,hover=True, size='sm')
        inact_table=dbc.Table.from_dataframe(inactive_mem, striped=True, bordered=True,hover=True, size='sm')
        new_table=dbc.Table.from_dataframe(new_mem, striped=True, bordered=True,hover=True, size='sm')
        reaff_table=dbc.Table.from_dataframe(reaff_mem, striped=True, bordered=True,hover=True, size='sm')
         #first we get the performance table
        sql='SELECT committee_id,CAST(evaluation as float8) FROM performance' #the cast in the sql is a function to convert the column from char(255) to a double precision (or float 8)
        cols=['hid','eval']
        hs_df=db.querydatafromdatabase(sql,[],cols)
        #we then get the average using df builtin function
        headship_average=hs_df.groupby('hid')['eval'].mean().round(3)
        #for table purposes we initiate the table names, and since it is static, we can just type it here
        committee_names=['Academic Affairs','External Affairs','Finance','Internal Affairs','Membership and Recruitment','Publications and Record']
        #since we removed the committee ID from active we are to refilter another one with only full name and committee id connected to them
        hs_active_mem=df[df['active']=='Active'][['Full Name','committee_id','gwa']]
        #add committee names for each id
        hs_active_mem['Committee Name']=[committee_names[int(cid)-1] if not math.isnan(cid) else "No Committee" for cid in hs_active_mem['committee_id']]
        # We now add the grading for each committee id
        hs_active_mem['Performance Grade']=[headship_average[int(cid)] if not math.isnan(cid) else 1 for cid in hs_active_mem['committee_id']] #assumme 1 muna yung lowest for performance checking lang
        #we create a new row
        #we now drop the committee id
        hs_active_mem=hs_active_mem.drop(columns=['committee_id'])
        all_table=dbc.Table.from_dataframe(hs_active_mem.drop(columns=['gwa']),striped=True, bordered=True,hover=True, size='sm')
        af_table=dbc.Table.from_dataframe(hs_active_mem[hs_active_mem['Committee Name']=='Academic Affairs'].drop(columns=['gwa']),striped=True, bordered=True,hover=True, size='sm')
        ef_table=dbc.Table.from_dataframe(hs_active_mem[hs_active_mem['Committee Name']=='External Affairs'].drop(columns=['gwa']),striped=True, bordered=True,hover=True, size='sm')
        f_table=dbc.Table.from_dataframe(hs_active_mem[hs_active_mem['Committee Name']=='Finance'].drop(columns=['gwa']),striped=True, bordered=True,hover=True, size='sm')
        if_table=dbc.Table.from_dataframe(hs_active_mem[hs_active_mem['Committee Name']=='Internal Affairs'].drop(columns=['gwa']),striped=True, bordered=True,hover=True, size='sm')
        mr_table=dbc.Table.from_dataframe(hs_active_mem[hs_active_mem['Committee Name']=='Membership and Recruitment'].drop(columns=['gwa']),striped=True, bordered=True,hover=True, size='sm')
        pr_table=dbc.Table.from_dataframe(hs_active_mem[hs_active_mem['Committee Name']=='Publications and Record'].drop(columns=['gwa']),striped=True, bordered=True,hover=True, size='sm')
        no_table=dbc.Table.from_dataframe(hs_active_mem[hs_active_mem['Committee Name']=='No Committee'].drop(columns=['gwa']),striped=True, bordered=True,hover=True, size='sm')

        #for the cards in headship, we add the number of members per committee thus we have and design it of some sort
        committee_val=[]
        for committee in committee_names+['No Committee']:
            committee_val+=[[html.H1(hs_active_mem[hs_active_mem['Committee Name']==committee].shape[0]),html.P("Active Members")]]


        ##next is for the member lists, this will include only those active and will not bother with the inactive ones/ can change if requested
        #first we filter the active members
        mem_list=df[df['active']=='Active']
        #in here we generate the child for the tab of by committee
        com_tab=[
            dbc.Tab([dbc.Container(dbc.Table.from_dataframe(df[df['committee_id']==i+1].drop(columns=['active','new','committee_id','gwa'])),class_name='sm-table-wrapper')],label=j)
            for i,j in enumerate(committee_names)
        ]
        com_tabs=dbc.Tabs(com_tab)
        #next is by year level
        #first we get the non empty unique year levels
        years=sorted(set(df['Year Standing'].unique())-{None})
        year_tab=[
            dbc.Tab([dbc.Container(dbc.Table.from_dataframe(df[df['Year Standing']==i].drop(columns=['active','new','committee_id','gwa'])),class_name='sm-table-wrapper')],label=i)
            for i in years
        ]
        year_tabs=dbc.Tabs(year_tab)
        #next is by appbatch
        #similar to years, we get non empty unique batches
        batches=sorted(list(set(df['App Batch'].unique())-{None}))
        batch_tab=[
            dbc.Tab([dbc.Container(dbc.Table.from_dataframe(df[df['App Batch']==i].drop(columns=['active','new','committee_id','gwa'])),class_name='sm-table-wrapper')],label=i)
            for i in batches
        
        ]
        app_tabs=dbc.Tabs(batch_tab)
        # here we generate the preference table
        #first we get identifiers: fullname, vlid id, and the preferences
        #NOTE: We will not need the current committee id since it is bound to change based on preferences
        sql="""
            SELECT person.valid_id,CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name, comm_firstchoice,comm_secondchoice,comm_thirdchoice,comm_fourthchoice,comm_fifthchoice,comm_sixthchoice
            FROM 
            person LEFT JOIN upciem_member 
            ON person.valid_id=upciem_member.valid_id JOIN affiliation 
            ON person.valid_id=affiliation.valid_id 
            WHERE (upciem_member_delete is NULL or upciem_member_delete=False) AND 
			active_status='Active'
        """#will only include active members (aka reaffiliated)
        cols=['Full Name','first','sec','third','frth','ffth','sth']
        com_df=db.querydatafromdatabase(sql,[],cols)

        #distribution type
        com_limit=com_df.shape[0]//6+bool(com_df.shape[0]%6>0) #will do a +1 when it cannot evenly distribute all members to have a max of com_limit+1 per pref

        
        #add those who hase prefernces using first preference first
        

        ##This is for the 14 Stripes,using the headship from active earlier
        ws_children=[]
        fteen_df=hs_active_mem.iloc[:]# just creating a copy just in case
        fteen_df['gwa']=pd.to_numeric(fteen_df['gwa'], errors='coerce')
        fteen_df['WS Scores']=round((fteen_df['gwa']+fteen_df['Performance Grade'])/2,3)
        fteen_df=fteen_df.sort_values(by='WS Scores',ascending=True)
        print(fteen_df.dtypes)
        # we now output them as table
        ws_children+=[html.H5("White Stripe Scores"),dbc.Container([dbc.Table.from_dataframe(fteen_df.drop(columns=['gwa','Performance Grade']),striped=True, bordered=True,hover=True, size='sm')],class_name='sm-table-wrapper')]
        fourteen=fteen_df.iloc[:14]#will only get first 14 regardless of ties, will fix if needed
        ws_children+=[html.H5("Top 14 White Stripe Members"),dbc.Container(dbc.Table.from_dataframe(fourteen.drop(columns=['gwa','Performance Grade','WS Scores','Committee Name']),striped=True, bordered=True,hover=True, size='xl'),class_name='ws-table-wrapper')]
        return new_reaff_children,act_inact_children,dash.no_update,act_table,inact_table,new_table,reaff_table,committee_val[0],committee_val[1],committee_val[2],committee_val[3],committee_val[4],committee_val[5],committee_val[6],af_table,ef_table,f_table,if_table,mr_table,pr_table,no_table,all_table,com_tabs,year_tabs,app_tabs,ws_children
    raise PreventUpdate
