# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:16:29 2019

@author: U6035631
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import eikon as ek
import json
import pandas as pd
import dash_bootstrap_components as dbc
import time
import dash_table as dt
import numpy as np
from business_duration import businessDuration
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import scipy.interpolate
import Func


i=0
num=5

navbar = dbc.NavbarSimple(id='nav-bar',
    children=[
        # dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Links",
            children=[
                dbc.DropdownMenuItem("Git",href='https://github.com/PedroAMBH/Eikon_API_Oprions_Dash_App'),
                dbc.DropdownMenuItem("Linkedin",href='https://www.linkedin.com/in/pedroalexandremoura/?locale=en_US'),
            ],
        ),
    ],
    brand="Refinitiv Eikon API - Options Dash (Alpha)",
    brand_href="https://community.developers.thomsonreuters.com",
    sticky="top",dark=True, color="#001eff",
)

# https://www.linkedin.com/in/pedroalexandremoura/?locale=en_US
# https://community.developers.thomsonreuters.com
# refinitiv.com



KeyLog=dbc.Card(
        dbc.CardBody([
                    html.H4('Eikon API key', className="card-title"),
                    dbc.Row(
                        [
                        dbc.Col(
                        dbc.Input(id='input-box0',
                                    placeholder='Enter a key...', 
                                    type='text',size=180,
                                    value='')),
                        dbc.Col(
                        dbc.Button('Submit', 
                                    id='button0',
                                    color="primary")),
                            ]),

                        dbc.Col(
                            html.P(id='output-container-key',
                                     children='Enter a Chain',className="card-text")
                                )
                        ],
                    className="w-80 mb-1"),
                color="dark",outline=True,inverse=False,
                style={"height" : "140px", 
                        "width" : "770px"},
            )


RicLoad=dbc.Card(
            dbc.CardBody([
                        html.H4('Options Chains', className="card-title"),
                        html.Div(
                            dcc.Input(id='input-box1', 
                                    type='text',
                                    value='0#PETR4*.SA')
                                ),

                        dbc.Row([
                            dbc.Col(
                            dbc.Button('Submit', 
                                        id='button1',
                                        color="primary")),
                            dbc.Col(
                                ##loading elemente
                                html.Div(id='Output-loading'),
                            ),
                        ]),

                        html.Div(id='output-container-Chain', 
                                style={'display': 'none'},
                                ),
                        ]),color="dark",outline=True,inverse=False,
                style={"height" : "140px", 
                        "width" : "260px"}
            )

DropD=dbc.Card(
            dbc.CardBody([

                html.H5('Options filter', className="card-title"),
                    html.Div(id='output-container-Dates', 
                                        style={'display': 'none'}
                                        ),
                    dbc.Row([
                        dbc.Col(  
                            html.Div([html.P('Select Maturities'),

                            dcc.Dropdown(id='output-container-DropD',
                                        multi=True,
                                        value=[],
                                        style={'width': '100%',
                                               'display': 'inline-block',
                                               },
                                        ),

                            html.Div(id='output-container-STATE'),
                        ])),
                        dbc.Col(
                            html.Div([html.P('Numero de Deltas'),
                                    dbc.Input(id='input-box3', 
                                              type='number',
                                              placeholder='Numero de Expitarions...'),
                                    ]),
                            ),
                        ]),
                        dbc.Button('Submit',
                                    color="primary", 
                                    id='button2'),
                        html.Div(id='output-container-Filter',children=None, 
                                style={'display': 'none'},
                                ),
                    ]),
                color="dark",outline=True,inverse=False,
            )


OptionsSelect=html.Div([
                dbc.Button(
                    "Suppress",
                    id="collapse-button",
                    className="mb-3",
                    color="primary",                    
                    ),

                html.Div(id='output-date-len',
                        # style={'display': 'none'},
                        ),

                dbc.Collapse(
                    dbc.Card(
                        dbc.CardBody([
                            html.Hr(id="line"),
                            dbc.Row([
                                dbc.Col(
                                    html.Div([
                                        html.P('CALL'),
                                        html.Div(id='Options_Call_selection'),
                                        html.Div(
                                                dbc.Card(
                                                    dbc.CardBody([dbc.Row(
                                                                            [dbc.Col([
                                                                                html.Div(id='datacall-{}'.format(i)),
                                                                                        dcc.Checklist(
                                                                                            id='List-options-call-{}'.format(i),className='radiobtn',
                                                                                            values=[],labelStyle={'display': 'list-item'},style={'display': 'inline-block'},
                                                                                            )
                                                                                    ],id='colcall-{}'.format(i),style={'display': 'none'}) for i in range(num)],
                                                                        )
                                                                    ]
                                                                ),color="primary", outline=True,id="callCard",style={"background": "linear-gradient(180deg, #57E35B 54%, #FEFEFE 46%)"},
                                                        ),
                                                    ),
                                    ])
                                    ),
                                dbc.Col(
                                    html.Div([
                                        html.P('PUT'),
                                        html.Div(id='Options_Put_selection'),
                                         html.Div(
                                                dbc.Card(
                                                    dbc.CardBody([dbc.Row(
                                                                            [dbc.Col([
                                                                                html.Div(id='dataput-{}'.format(i)),
                                                                                        dcc.Checklist(
                                                                                            id='List-options-put-{}'.format(i),className='radiobtn',
                                                                                            values=[],labelStyle={'display': 'list-item'},style={'display': 'inline-block'},
                                                                                            )
                                                                                    ],id='colput-{}'.format(i),style={'display': 'none'}) for i in range(num)],
                                                                        )
                                                                    ]
                                                                ),color="danger", outline=True,id="putCard",style={"background": "linear-gradient(180deg, #FEFEFE 54%, #ee7676 46%)"},
                                                        ),
                                                    ),
                                    ])),
                                ]),
                            ])
                        ),
                    id="collapse",
                ),
            ]
            )



TableM=dbc.Card(
            dbc.CardBody([
                html.H5('Options Strategy', className="card-title"),
                html.Div(id='output-tabela-select', 
                                    style={'display': 'none'},
                                    ),
                html.Div([
                    html.Div(id="Chart_0"),
                    html.Div(id="Total-net-trade"),
            ])
            ],
        ),color="dark",outline=True,
    )




ChartAn=dbc.Card(
            dbc.CardBody([
                html.H5('Strategy Chart', className="card-title"),
                html.Div(id='output-memory_str', 
                                    style={'display': 'none'},
                                    ),
                html.Div(id='output-Proba', 
                                    ),
                html.Div([
                    dcc.Graph(id='output-chart-strategy',animate=True,
                            style={'height': '550px'},
                        ),
                    ]),
                ])
        )



### Key
body=dbc.Container(
    [
        dbc.Row([
                dbc.Col(KeyLog),
                dbc.Col(RicLoad,width=3)
                ]),
        html.Br(),
        dbc.Row([
                dbc.Col(DropD,width=12),
                ]),
        html.Hr(),
        dbc.Row([
                dbc.Col(OptionsSelect),
                ]),
        html.Hr(),
        dbc.Row([
                dbc.Col(TableM),
                ]),
                html.Hr(),
        dbc.Row([
                dbc.Col(ChartAn),
                ]),
    ])




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([navbar,
                        html.Br(),
                        body])



### logando 
@app.callback(
    dash.dependencies.Output('output-container-key', 'children'),
    [dash.dependencies.Input('button0', 'n_clicks')],
    [dash.dependencies.State('input-box0', 'value')])
def logkey(n_clicks,value):
    if n_clicks!=None:
        ek.set_app_key(value)
        ek.set_timeout(60*5)
        return 'Confirm: "{}"'.format(value)


@app.callback(
    dash.dependencies.Output('output-container-Chain', 'children'),
    [dash.dependencies.Input('button1', 'n_clicks')],
    [dash.dependencies.State('input-box1', 'value')],)
def update_values(n_clicks, value):
    if (n_clicks!=None)&(value!=None):
        lista, err = ek.get_data(value,'RData')
        lista=lista.Instrument[~lista.Instrument.isnull()].values
        optionsInfo, err = ek.get_data(list(lista),['TRADE_DATE','TRDPRC_1',"PUTCALLIND","EXPIR_DATE","STRIKE_PRC","IMP_VOLT","BKGD_REF"])
        optionsInfo=optionsInfo[optionsInfo.STRIKE_PRC.notnull()]
        optionsInfo=optionsInfo[optionsInfo.EXPIR_DATE.astype('datetime64')>=optionsInfo.TRADE_DATE.astype('datetime64').max()]
        spot, err = ek.get_data([optionsInfo.BKGD_REF.values[0]]+['BRSELICD=CBBR'],['TRADE_DATE','TRDPRC_1'])
        # print(optionsInfo.head())
        optionsInfo['Delta']=spot.TRDPRC_1.values[0]-optionsInfo.STRIKE_PRC
        optionsInfo_C=optionsInfo[optionsInfo.PUTCALLIND=='CALL']
        optionsInfo_P=optionsInfo[optionsInfo.PUTCALLIND!='CALL']
        
        RE={"optionsInfo":optionsInfo.to_json(),
            "optionsInfo_C":optionsInfo_C.to_json(),
            "optionsInfo_P":optionsInfo_P.to_json(),
            "spot":spot.to_json()}

        return (json.dumps(RE))
    else:
        return (None)


## Carregando dados 
@app.callback(
    dash.dependencies.Output('Output-loading', 'children'),
    [dash.dependencies.Input('button1', 'n_clicks')])
def update_values(n_clicks,):
    if n_clicks!=None:
        return(html.Div(
                dbc.Spinner(color="primary",
                type="grow"),
            style={'display': 'inline-block'},
            id='loading-id'))



## Carregando dados 
@app.callback(
    dash.dependencies.Output('loading-id', 'style'),
    [dash.dependencies.Input('output-container-Chain', 'children')])
def update_values(value):
    return {'display': 'none'}



@app.callback(
    dash.dependencies.Output("collapse", "is_open"),
    [dash.dependencies.Input("collapse-button", "n_clicks")],
    [dash.dependencies.State("collapse", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open




@app.callback(
    dash.dependencies.Output('Chart_0', 'children'),
    [dash.dependencies.Input('button2', 'n_clicks')],
)
def UppCh(n_clicks):
    if n_clicks!=None:
        return (dbc.Row([
                    dbc.Col(
                        dt.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in ["Instrument","Day","Price","type","Maturity","Strike","Amount","ImpVol"]],
                            data=pd.DataFrame([],columns=["Instrument","Day","Price","type","Maturity","Strike","Amount"]).to_dict('records'),
                            editable=True,
                            row_selectable="multi",
                            sorting_type="multi",
                            # row_deletable=True,
                            selected_rows=[],
                            style_cell={'minHeight': '30px', 'height': '30px', 'maxHeight': '30px',
                                        'whiteSpace': 'normal'},
                        ),width=7),

                    dbc.Col(
                        dt.DataTable(
                            id='table1',
                            columns=[{"name": i, "id": i} for i in ['Financial','Delta','Gamma','Vega','Theta','Rho']],
                            data=pd.DataFrame([],columns=['Financial','ImpVol','Delta','Gamma','Vega','Theta','Rho']).to_dict('records'),
                            style_cell={'minHeight': '30px', 'height': '30px', 'maxHeight': '30px',
                                        'minWidth': '60px', 'width': '60px', 'maxWidth': '60px',
                                        'whiteSpace': 'normal'},
                            # fixed_rows={ 'headers': True, 'data': 0 },
                        ),
                    ),                  
                    ])
                )
    else:
        return ("")




@app.callback(
    dash.dependencies.Output('output-container-DropD', 'options'),
    [dash.dependencies.Input('output-container-Chain', 'children'),
    dash.dependencies.Input('loading-id', 'style')])
def DropD(children,style):
    optionsInfo=pd.DataFrame(json.loads(json.loads(children)['optionsInfo']))
    lldate=list(set(optionsInfo.EXPIR_DATE.values))
    lldate.sort()
    DropD=[{"label":i,"value":i} for i in lldate]
    return DropD



@app.callback(
    dash.dependencies.Output('output-container-Filter', 'children'),
    [dash.dependencies.Input('button2', 'n_clicks')],
    [dash.dependencies.State('input-box3', 'value'),
     dash.dependencies.State('output-container-DropD', 'value'),
     dash.dependencies.State('output-container-Chain', 'children')])
def FilDelta(n_clicks,value1,lid,children):
    if (n_clicks!=None)&(value1!=None)&(lid!=None)&(children!=None):
        optionsInfo_C=pd.DataFrame(json.loads(json.loads(children)['optionsInfo_C']))
        optionsInfo_P=pd.DataFrame(json.loads(json.loads(children)['optionsInfo_P']))
        optionsInfo=pd.DataFrame(json.loads(json.loads(children)['optionsInfo']))

        optionsInfo=optionsInfo.sort_values('STRIKE_PRC')
        optionsInfo_C=optionsInfo_C.sort_values('STRIKE_PRC')
        optionsInfo_P=optionsInfo_P.sort_values('STRIKE_PRC')

        optionsInfo.index=range(len(optionsInfo))
        optionsInfo_C.index=range(len(optionsInfo_C))
        optionsInfo_P.index=range(len(optionsInfo_P))

        # lldate=list(set(optionsInfo.EXPIR_DATE.values))
        # lldate.sort()
        lid.sort()
        lldate=lid
        Selec_C=Func.DeltaStreikFilter(optionsInfo_C,lldate,value1)
        Selec_P=Func.DeltaStreikFilter(optionsInfo_P,lldate,value1)

        callRIC=pd.DataFrame(Selec_C).T
        callRIC.columns=lldate

        call=pd.DataFrame([optionsInfo[optionsInfo.Instrument.isin(Selec_C[i])].STRIKE_PRC.values for i in range(len(Selec_C))]).T
        call.columns=lldate

        putRIC=pd.DataFrame(Selec_P).T
        putRIC.columns=lldate
        put=pd.DataFrame([optionsInfo[optionsInfo.Instrument.isin(Selec_P[i])].STRIKE_PRC.values for i in range(len(Selec_P))]).T
        put.columns=lldate
        RE={"callRIC":callRIC.to_json(),
            "call":call.to_json(),
            "putRIC":putRIC.to_json(),
            "put":put.to_json(),}

        return (json.dumps(RE))
    else:
        return(None)






### --- omit Elements
@app.callback(
    [dash.dependencies.Output('colcall-{}'.format(i), 'style') for i in range(num)],
    [dash.dependencies.Input('button2', 'n_clicks')],
    [dash.dependencies.State('output-container-DropD', 'value')],
    )
def datcall0(n_clicks,children):
    if (n_clicks!=None) & (children!=None):
        children.sort()
        le=[]
        for j in range(num):
            if j<=(len(children)-1):
                le=le+[{'display': 'inline-block'}]
            else:
                le=le+[{'display': 'none'}]
        return le
    else:
        return [{'display': 'none'}  for i in range(num)]



@app.callback(
    [dash.dependencies.Output('colput-{}'.format(i), 'style') for i in range(num)],
    [dash.dependencies.Input('button2', 'n_clicks')],
    [dash.dependencies.State('output-container-DropD', 'value')],
    )
def datput0(n_clicks,children):
    if (n_clicks!=None) & (children!=None):
        children.sort()
        le=[]
        for j in range(num):
            if j<=(len(children)-1):
                le=le+[{'display': 'inline-block'}]
            else:
                le=le+[{'display': 'none'}]
        return le
    else:
        return [{'display': 'none'}  for i in range(num)]        



### ---------- Values


@app.callback(
    [dash.dependencies.Output('List-options-call-{}'.format(i), 'values') for i in range(num)]+\
    [dash.dependencies.Output('List-options-put-{}'.format(i), 'values') for i in range(num)],
    [dash.dependencies.Input('button2', 'n_clicks')],
    # [dash.dependencies.State('output-container-DropD', 'values')],
    )
def datcall1(n_clicks):
    return [[]  for i in range(num*2)]



### --- Get Date lable
@app.callback(
    [dash.dependencies.Output('datacall-{}'.format(i), 'children') for i in range(num)],
    [dash.dependencies.Input('button2', 'n_clicks')],
    [dash.dependencies.State('output-container-DropD', 'value')],
    )
def datcall2(n_clicks,children):
    if (n_clicks!=None) & (children!=None):
        children.sort()
        le=[]
        for j in range(num):
            if j<=(len(children)-1):
                le=le+[html.P(children[j])]
            else:
                le=le+[""]
        return le
    else:
        return [""  for i in range(num) ]        

@app.callback(
    [dash.dependencies.Output('dataput-{}'.format(i), 'children') for i in range(num)],
    [dash.dependencies.Input('button2', 'n_clicks')],
    [dash.dependencies.State('output-container-DropD', 'value')],
    )
def datput2(n_clicks,children):
    if (n_clicks!=None) & (children!=None):
        children.sort()
        le=[]
        for j in range(num):
            if j<=(len(children)-1):
                le=le+[html.P(children[j])]
            else:
                le=le+[""]
        return le
    else:
        return [""  for i in range(num) ]        


### --- Get Options for select

@app.callback(
    [dash.dependencies.Output('List-options-call-{}'.format(i), 'options') for i in range(num)],
    # [dash.dependencies.Input('button2', 'n_clicks')],
    [dash.dependencies.Input('output-container-Filter', 'children')],
    )
def datcall3(children):
    if (children!=None):
        callRIC=pd.DataFrame(json.loads(json.loads(str(children))['callRIC']))
        call=pd.DataFrame(json.loads(json.loads(str(children))['call']))

        callRIC.index=(callRIC.index.astype(int))
        call.index=(call.index.astype(int))
        callRIC=callRIC.sort_index()
        call=call.sort_index()

        le=[]
        c=0
        for c in range(num):
            if c<=(len(call.columns)-1):
                options=[{'label':ii,'value':jj} for ii,jj in zip(call.values[:,c],callRIC.values[:,c])]
                le=le+[options]
            else:
                options1=[{'label':0,'value':0}]
                le=le+[options1]
        return(le)

    else:
        return [[{'label':0,'value':0}]  for i in range(num)]


@app.callback(
    [dash.dependencies.Output('List-options-put-{}'.format(i), 'options') for i in range(num)],
    [dash.dependencies.Input('output-container-Filter', 'children')],
    )
def datput3(children):
    if (children!=None):
        putRIC=pd.DataFrame(json.loads(json.loads(str(children))['putRIC']))
        put=pd.DataFrame(json.loads(json.loads(str(children))['put']))

        putRIC.index=(putRIC.index.astype(int))
        put.index=(put.index.astype(int))
        putRIC=putRIC.sort_index()
        put=put.sort_index()

        le=[]
        c=0
        for c in range(num):
            if c<=(len(put.columns)-1):
                options=[{'label':ii,'value':jj} for ii,jj in zip(put.values[:,c],putRIC.values[:,c])]
                le=le+[options]
            else:
                options1=[{'label':0,'value':0}]
                le=le+[options1]
        return(le)

    else:
        return [[{'label':0,'value':0}]  for i in range(num)]



# #-------- Colect to Table
@app.callback(
    dash.dependencies.Output('output-tabela-select', 'children'),
    [dash.dependencies.Input('List-options-call-{}'.format(i), 'values') for i in range(num)]+\
    [dash.dependencies.Input('List-options-put-{}'.format(i), 'values') for i in range(num)],
)
def teste(*va):
    if (va!=None):
        if (len(va)==num*2):
            g=[]
            for x in (va):
                g=g+x
            va=g
        return (va)
    else:
        return ([])




@app.callback(
    [dash.dependencies.Output('table', 'data'),
    dash.dependencies.Output('table', 'selected_rows')],
    [dash.dependencies.Input('output-tabela-select', 'children')],
    [dash.dependencies.State('output-container-Chain', 'children')]
)
def TableUpdate(*va):
    if (len(va[0])>=1) & (va[-1]!=None):
        va=list(va)
        ListOP=va[:-1][0]
        children=va[-1]

        #### ---- Populating table
        optionsInfo_C=pd.DataFrame(json.loads(json.loads(str(children))['optionsInfo_C']))
        optionsInfo_P=pd.DataFrame(json.loads(json.loads(str(children))['optionsInfo_P']))
        optionsInfo=pd.DataFrame(json.loads(json.loads(str(children))['optionsInfo']))

        tabc=optionsInfo_C[optionsInfo_C.Instrument.isin(ListOP)][["Instrument","TRADE_DATE","TRDPRC_1","PUTCALLIND","EXPIR_DATE","STRIKE_PRC","IMP_VOLT"]]
        tabp=optionsInfo_P[optionsInfo_P.Instrument.isin(ListOP)][["Instrument","TRADE_DATE","TRDPRC_1","PUTCALLIND","EXPIR_DATE","STRIKE_PRC","IMP_VOLT"]]

        tabc=tabc.sort_values('STRIKE_PRC')
        tabp=tabp.sort_values('STRIKE_PRC')

        tabc.index=range(len(tabc))
        tabp.index=range(len(tabc),len(tabc)+len(tabp))
        tab=tabc.append(tabp)

        tab["Amount"]=0

        tab.columns=["Instrument","Day","Price","type","Maturity","Strike","ImpVol","Amount"]
        return ([tab.to_dict('rows'),[]])

    else:
        return [[],[]]






@app.callback(
    dash.dependencies.Output('table1', 'data'),
    # [dash.dependencies.Input('output-tabela-select', 'children')]+\
    [dash.dependencies.Input('table', 'data_timestamp')]+\
    [dash.dependencies.Input('table', 'data')],
    [dash.dependencies.State('output-container-Chain', 'children')]
)
def TableUpdate1(data_timestamp,data,children):
    #### ---- Populating table
    if (data_timestamp!= None)&(children!=None):
        if len(data)>0:
            data=pd.DataFrame(data)
            data['Amount']=data['Amount'].astype(float)
            data['Price']=data['Price'].astype(float)
            data['Strike']=data['Strike'].astype(float)
            data['ImpVol']=data['ImpVol'].astype(float)
            data["Day"]=pd.to_datetime(data["Day"])
            data["Maturity"]=pd.to_datetime(data["Maturity"])
            data["Financial"] = data['Amount']*data['Price']
            data["Financial"]=data["Financial"].round(2)

            spot=pd.DataFrame(json.loads(json.loads(str(children))['spot']))
            spot["TRADE_DATE"]=pd.to_datetime(spot["TRADE_DATE"])

            days=(data.apply(lambda row: businessDuration(startdate=row['Day'],enddate=row['Maturity'],unit='day'), axis=1)).values

            # ImpyVola=[round(Func.ImpliedVola(spot[spot["Instrument"]!="BRSELICD=CBBR"].TRDPRC_1.values[0].astype(float),
            #             data["Strike"].values[j].astype(float),
            #             spot[spot["Instrument"]=="BRSELICD=CBBR"].TRDPRC_1.values[0].astype(float)/100,
            #             .70,
            #             data["Price"].values[j].astype(float),
            #             days[j],
            #             data["type"],a=-12.0, b=12.0, xtol=1e-8)*100,2) for j in range(len(data))]
            ImpyVola=data['ImpVol'].values
            GREEKS=Func.OpitionsPrice(spot[spot["Instrument"]!="BRSELICD=CBBR"].TRDPRC_1.values[0].astype(float),
                                        data["Strike"].values.astype(float),
                                        spot[spot["Instrument"]=="BRSELICD=CBBR"].TRDPRC_1.values[0].astype(float)/100,
                                        np.array(ImpyVola)/100,
                                        days)

            data[['Valor','Delta','Gamma','Vega','Theta','Rho','Etas']]=pd.DataFrame([[0 for i in range(7)]], columns=['Valor','Delta','Gamma','Vega','Theta','Rho','Etas'],index=data.index)

            callGreek=GREEKS[list(GREEKS.columns[GREEKS.columns.str.contains('C', regex=True)])][data.type.str.contains('C', regex=True).values]
            putGreek=GREEKS[list(GREEKS.columns[GREEKS.columns.str.contains('P', regex=True)])][data.type.str.contains('P', regex=True).values]

            callGreek.columns=['Valor','Delta','Gamma','Vega','Theta','Rho','Etas']
            putGreek.columns=['Valor','Delta','Gamma','Vega','Theta','Rho','Etas']

            data.loc[list(data.type.str.contains('C', regex=True).values),['Valor','Delta','Gamma','Vega','Theta','Rho','Etas']]=round(callGreek,3).values
            data.loc[list(data.type.str.contains('P', regex=True).values),['Valor','Delta','Gamma','Vega','Theta','Rho','Etas']]=round(putGreek,3).values

            data["ImpVol"]=ImpyVola
            data["Delta"]=data.Delta.values
            data["Gamma"]=data.Gamma.values
            data["Vega"]=data.Vega.values
            data["Theta"]=data.Theta.values
            data["Rho"]=data.Rho.values
            return (data[['Financial','Delta','Gamma','Vega','Theta','Rho']].to_dict('records'))

        else:
            return []
 
    else:
        return []



@app.callback(
    dash.dependencies.Output('Total-net-trade', 'children'),
    [dash.dependencies.Input('table1', 'data')],
)
def CalcNet(data):
    if data!=None:
        if len(data)>0:
            data=pd.DataFrame(data)
            data['Financial']=data['Financial'].astype(float)
            return (html.H6('Cost:{}'.format(sum(data["Financial"].values)*-1)))
        else:
            return (html.H6(''))
    else:
        return (html.H6(''))



@app.callback(
    [dash.dependencies.Output('output-chart-strategy', 'figure'),
    dash.dependencies.Output('output-Proba', 'children')],
    [dash.dependencies.Input('table', 'selected_rows'),
    dash.dependencies.Input('table', 'data')],
    [dash.dependencies.State('output-container-Chain', 'children')]+\
    [dash.dependencies.State('input-box0', 'value')]
)
def CalcNetChart(row_ids,data,children,value):
    if (row_ids!=None)&(data!=None):
        if (len(row_ids)>0)&(len(data)>0):

            ek.set_app_key(value)
            ek.set_timeout(60*5)

            data=pd.DataFrame(data)
            data=data[data.index.isin(row_ids)]
            data['Amount']=data['Amount'].astype(float)
            data['Price']=data['Price'].astype(float)
            data['Strike']=data['Strike'].astype(float)
            data["Day"]=pd.to_datetime(data["Day"])
            data["Maturity"]=pd.to_datetime(data["Maturity"])

            data["Financial"] = data['Amount']*data['Price']
            data["Financial"]=data["Financial"].round(2)

            spot=pd.DataFrame(json.loads(json.loads(str(children))['spot']))
            spot['TRDPRC_1']=spot['TRDPRC_1'].astype(float)
            spot["TRADE_DATE"]=pd.to_datetime(spot["TRADE_DATE"])
            ssp=spot[spot["Instrument"]!="BRSELICD=CBBR"].TRDPRC_1.values[0]


            days=(data.apply(lambda row: businessDuration(startdate=row['Day'],enddate=row['Maturity'],unit='day'), axis=1)).values
            days=list(set(days))

            vola, err = ek.get_data([spot[spot["Instrument"]!="BRSELICD=CBBR"].Instrument.values[0]],
                                        ['TR.Volatility5D','TR.Volatility10D',"TR.Volatility20D",
                                        "TR.Volatility30D","TR.Volatility60D","TR.Volatility90D"])

            volaV=(sum((vola.T[0].values[1:]*(abs(np.array([5,10,20,30,60,90])-15)+1)/(sum(abs(np.array([5,10,20,30,60,90])-15)+1)))))/100

            vola.columns=['Instrument',5,10,20,30,60,90]
            vola[[5,10,20,30,60,90]]=vola[[5,10,20,30,60,90]]/100
            days=list(np.unique(days))
            dists=[]
            vollist=[]
            for d in days:
                y_interp = scipy.interpolate.interp1d(vola.columns[1:].astype(float),vola.T[0].values[1:].astype(float))
                volaV=y_interp(d)
                Distrib=1-np.random.normal(0,(volaV/(252**0.5)*(d**0.5)), size=5000)
                Distrib=Distrib*ssp

                vollist.append(volaV)
                dists.append(Distrib)

            Price=dists[pd.DataFrame(dists).max(1).argmax()]
            Price.sort()
            net=[]
            for k in range(len(data)):
                if data['Amount'].iloc[k]>=0:
                    if "C" in data['type'].iloc[k]:
                        Rt= -data['Strike'].iloc[k]-data['Price'].iloc[k] +Price
                        Rt[Rt<=-data['Price'].iloc[k]]=-data['Price'].iloc[k]
                        Rt=Rt*abs(data['Amount'].iloc[k])
                        net.append(list(Rt))
                    else:
                        Rt= data['Strike'].iloc[k] -data['Price'].iloc[k] -Price
                        Rt[Rt<=-data['Price'].iloc[k]]=-data['Price'].iloc[k]
                        Rt=Rt*abs(data['Amount'].iloc[k])
                        net.append(list(Rt))

                else:
                    if "C" in data['type'].iloc[k]:
                        Rt= data['Strike'].iloc[k] +data['Price'].iloc[k] -Price
                        Rt[Rt>=data['Price'].iloc[k]]=data['Price'].iloc[k]
                        Rt=Rt*abs(data['Amount'].iloc[k])
                        net.append(list(Rt))
                    else:
                        Rt= -data['Strike'].iloc[k] +data['Price'].iloc[k] +Price
                        Rt[Rt>=data['Price'].iloc[k]]=data['Price'].iloc[k]
                        Rt=Rt*abs(data['Amount'].iloc[k])
                        net.append(list(Rt))

            pay=pd.DataFrame(net)
            pay.columns=Price
            pays=pay
            # print(pays.values)
            pay=pay.sum()

            tempTT=[]
            for j in range(len(set(days))):
                tempT=[]
                for s in range(len(data["Strike"])):
                    temp=Func.OpitionsPrice(Price,
                                        data["Strike"].values.astype(float)[s],
                                        spot[spot["Instrument"]=="BRSELICD=CBBR"].TRDPRC_1.values[0].astype(float)/100,
                                        np.array(data['ImpVol'].values[j])/100,
                                        days[j])
                    
                    if "C" in data["PUTCALLIND"].values[s]:
                        temp=list((temp.ValorC.values-data['TRDPRC_1'].values[s])*data['Amount'].values[s])
                    else:
                        temp=list((temp.ValorP.values-data['TRDPRC_1'].values[s])*data['Amount'].values[s])

                    tempT.append(temp)

                tempTT.append(tempT)


            fig = go.FigureWidget(make_subplots(shared_xaxes=True, specs=[[{"secondary_y": True}]],print_grid=False))
            trace3 = go.Scatter(name="0 line",x=pay.index,
                                   y=np.array([0 for i in Distrib]),
                                   xaxis = 'x1',yaxis = 'y2',
                                   line = dict(color='black', width=2, dash='dash'))
            fig.add_trace(trace3, secondary_y=False)

            trace1 = go.Scatter(name="Payoff",x=pay.index,
                                   y=pay.values,xaxis = 'x1',yaxis = 'y2',
                                   mode='lines',fill='tozeroy')
            fig.add_trace(trace1, secondary_y=False)

            for i in range(len(tempTT)):
                trace5 = go.Scatter(name="Price - "+str(days[i])+' Days',x=pay.index,
                                       y=pd.DataFrame(tempTT[i]).sum().values,
                                       xaxis = 'x1',yaxis = 'y2',
                                       mode='lines')
                fig.add_trace(trace5, secondary_y=False)


            for lin,i in zip(pays.values,pays.index):
                trace4 = go.Scatter(name=data.Instrument.values[i],x=pay.index,
                                       y=lin,xaxis = 'x1',yaxis = 'y2',
                                       line = dict(width=2, dash='dash'))
                fig.add_trace(trace4, secondary_y=False)


            for i,j in zip(days,dists):
                trace2 = ff.create_distplot([j],[str(i)+" Days - Probabilidade"], bin_size=.5,curve_type='normal',show_hist=False,show_rug=False)
                fig.add_trace(trace2['data'][0], secondary_y=True)

            prob=round(sum(pay.values>0)/len(Distrib)*100,2)
            return [fig, html.H6("Profit probability: "+str(prob)+"%")]

        else:
            fig = go.FigureWidget(make_subplots(shared_xaxes=True, specs=[[{"secondary_y": True}]],print_grid=False))

            trace3 = go.Scatter(name="0 line",x=[0],
                                   y=[0],
                                   xaxis = 'x1',yaxis = 'y2',
                                   line = dict(color='black', width=2, dash='dash'))

            fig.add_trace(trace3, secondary_y=False)

            return [fig, html.H6(str(0)+"%")]

    else:

        fig = go.FigureWidget(make_subplots(shared_xaxes=True, specs=[[{"secondary_y": True}]],print_grid=False))

        trace3 = go.Scatter(name="0 line",x=[0],
                               y=[0],
                               xaxis = 'x1',yaxis = 'y2',
                               line = dict(color='black', width=2, dash='dash'))

        fig.add_trace(trace3, secondary_y=False)

        return [fig, html.H6(str(0)+"%")]
























if __name__ == "__main__":
    app.run_server(debug=True)



