import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import eikon as ek
import json
import pandas as pd
import dash_bootstrap_components as dbc
import time
import Func
import dash_table as dt
import numpy as np

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    brand="Option App",
    brand_href="#",
    sticky="top",
)


KeyLog=dbc.Card(
        dbc.CardBody([
                    html.H4('Eikon key', className="card-title"),
                    dbc.Row(
                        [
                        dbc.Col(
                        dbc.Input(id='input-box0',
                                    placeholder='Enter a key...', 
                                    type='text',size=180,
                                    value='b62c1ab67f2d457980440a42dbe099dd868d6a29')),
                        dbc.Col(
                        dbc.Button('Submit', 
                                    id='button0',
                                    color="primary")),
                            ]),

                        dbc.Col(
                            html.P(id='output-container-key',
                                     children='Enter a Chain')
                                )
                        ],
                    className="w-80 mb-1"),
                color="dark",inverse=True,
                # style={"w": "120rem",
                #         "b":"15rem"},
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
                                # children=None,
                                style={'display': 'none'},
                                ),
                        ]),color="dark",inverse=True,
                style={"height" : "140px", 
                        "width" : "260px"}
            )

DropD=dbc.Card(
            dbc.CardBody([

                html.H5('Filtro de data', className="card-title"),
                    html.Div(id='output-container-Dates', 
                                        style={'display': 'none'}
                                        ),
                    dbc.Row([
                        dbc.Col(  
                            html.Div([html.P('Selecione Vencimentos'),

                            dcc.Dropdown(id='output-container-DropD',
                                        multi=True,
                                        value=[],
                                        style={'width': '100%',
                                               'display': 'inline-block',
                                               # 'text': '1111111',
                                               # # 'background': '#7FDBFF',
                                               # 'DEM': '#0000FF',
                                               # 'VirtualizedSelectFocusedOption': '#FF0000',
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
                color="dark",inverse=True,
            )


OptionsSelect=html.Div([
                dbc.Button(
                    "Suprimir opções",
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
                            dbc.Row([

                                dbc.Col(
                                    html.Div([
                                        html.P('CALL'),
                                        html.Div(id='Options_Call_selection')


                                        ,
                                    ])),
                                dbc.Col(
                                    html.Div([
                                        html.P('PUT'),
                                        html.Div(id='Options_Put_selection'),
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
                html.H5('Operações', className="card-title"),
                html.Div(id='output-tabela-select', 
                                    # style={'display': 'none'}
                                    ),
                html.Div(
                    dt.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in ['TRADE_DATE','TRDPRC_1',"PUTCALLIND","EXPIR_DATE","STRIKE_PRC","Position*","Position$"]],
                        # rows=[{"name": i, "id": i} for i in ['TRADE_DATE','TRDPRC_1',"PUTCALLIND","EXPIR_DATE","STRIKE_PRC","Position*"]],
                        editable=True,
                        # fixed_rows={ 'headers': True, 'data': 0 },
                        ),
                    ),
                ]),
                color="dark",outline=True,
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
                ])
    ])








app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
# app.scripts.config.serve_locally = False

# app.config['suppress_callback_exceptions']=True
app.config.suppress_callback_exceptions = True

# app.css.append_css({
#     'external_url': 'https://raw.githubusercontent.com/tcbegley/dash-bootstrap-css/master/dist/darkly/bootstrap.css'
#     })




app.layout = html.Div([navbar,body])



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
        # time.sleep(3)
        lista, err = ek.get_data(value,'RData')
        lista=lista.Instrument[~lista.Instrument.isnull()].values
        optionsInfo, err = ek.get_data(list(lista),['TRADE_DATE','TRDPRC_1',"PUTCALLIND","EXPIR_DATE","STRIKE_PRC","BKGD_REF"])
        optionsInfo=optionsInfo[optionsInfo.STRIKE_PRC.notnull()]
        optionsInfo=optionsInfo[optionsInfo.EXPIR_DATE.astype('datetime64')>=optionsInfo.TRADE_DATE.astype('datetime64').max()]
        spot, err = ek.get_data([optionsInfo.BKGD_REF.values[0]]+['BRSELICD=CBBR'],['TRADE_DATE','TRDPRC_1'])
        optionsInfo['Delta']=spot.TRDPRC_1.values[0]-optionsInfo.STRIKE_PRC
        optionsInfo_C=optionsInfo[optionsInfo.PUTCALLIND=='CALL']
        optionsInfo_P=optionsInfo[optionsInfo.PUTCALLIND!='CALL']
        RE={"optionsInfo":optionsInfo.to_json(),
            "optionsInfo_C":optionsInfo_C.to_json(),
            "optionsInfo_P":optionsInfo_P.to_json(),
            "spot":spot.to_json()}
        # lldate=list(set(optionsInfo.EXPIR_DATE.values))
        # lldate.sort()
        # return (RE)
        return (json.dumps(RE))
        # return(str(value))
    else:
        return (' ')


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
    # if type(value)=='str':
    return {'display': 'none'}




# @app.callback(
#     dash.dependencies.Output("collapse", "is_open"),
#     [dash.dependencies.Input("Selecione-Collapsible", "n_clicks")],
#     [dash.dependencies.State("collapse", "is_open")],
#     )
# def toggle_collapse(n, is_open):
#     if (n_clicks!=None):
#         if n%2==0:
#             return not is_open
#         else:
#            return is_open
#     else:
#         return is_open



@app.callback(
    dash.dependencies.Output("collapse", "is_open"),
    [dash.dependencies.Input("collapse-button", "n_clicks")],
    [dash.dependencies.State("collapse", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open





# @app.callback(
#     dash.dependencies.Output('output-container-STATE', 'children'),
#     [dash.dependencies.Input('output-container-Chain', 'children')])
# def Loaded(children):
#     if children!=None:
#     # optionsInfo=pd.DataFrame(json.loads(json.loads(children)['optionsInfo']))
#     # lldate=list(set(optionsInfo.EXPIR_DATE.values))
#     # lldate.sort()
#     # DropD=[{"label":i,"value":i} for i in lldate]
#         return dbc.Alert("Completo", color="success")


@app.callback(
    dash.dependencies.Output('output-container-DropD', 'options'),
    [dash.dependencies.Input('output-container-Chain', 'children'),
    dash.dependencies.Input('loading-id', 'style')])
def DropD(children,style):
    optionsInfo=pd.DataFrame(json.loads(json.loads(children)['optionsInfo']))
    lldate=list(set(optionsInfo.EXPIR_DATE.values))
    lldate.sort()
    DropD=[{"label":i,"value":i} for i in lldate]
    # DropD=[{"label":i,"value":i} for i in range(5)]
    return DropD



@app.callback(
    dash.dependencies.Output('output-container-Filter', 'children'),
    [dash.dependencies.Input('button2', 'n_clicks')],
    # [dash.dependencies.State('input-box2', 'value'),
     [dash.dependencies.State('input-box3', 'value'),
     dash.dependencies.State('output-container-DropD', 'value'),
     dash.dependencies.State('output-container-Chain', 'children')])
def FilDelta(n_clicks,value1,lid,children):
    if (n_clicks!=None)&(value1!=None)&(lid!=None)&(children!=None):
        optionsInfo_C=pd.DataFrame(json.loads(json.loads(children)['optionsInfo_C']))
        optionsInfo_P=pd.DataFrame(json.loads(json.loads(children)['optionsInfo_P']))
        optionsInfo=pd.DataFrame(json.loads(json.loads(children)['optionsInfo']))

        # lldate=list(set(optionsInfo.EXPIR_DATE.values))
        # lldate.sort()
        lid.sort()
        lldate=lid
        Selec_C=Func.DeltaStreikFilter(optionsInfo_C,lldate,value1)
        Selec_P=Func.DeltaStreikFilter(optionsInfo_P,lldate,value1)

        callRIC=pd.DataFrame(Selec_C).T
        callRIC.columns=lldate
        # return(str(value0),str(value1),str(callRIC.columns[0]))
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



# @app.callback(
#     dash.dependencies.Output('table', 'columns'),
#     [dash.dependencies.Input('output-container-Chain', 'children')]
# )
# def Columns(children):
#     if children!=None:
#         optionsInfo=pd.DataFrame(json.loads(json.loads(str(children))['optionsInfo']))
#         columns=[{"name": i, "id": i} for i in optionsInfo.columns]
#         retunr(columns)




@app.callback(
    dash.dependencies.Output('Options_Call_selection', 'children'),
    [dash.dependencies.Input('output-container-Filter', 'children')])
def GridOptions(children):
    if children!=None:
        # return str(children)
        callRIC=pd.DataFrame(json.loads(json.loads(str(children))['callRIC']))
        call=pd.DataFrame(json.loads(json.loads(str(children))['call']))

        html0=[]
        for i in range(len(call.columns)):
            html0=html0+[dbc.Col([
                                    html.P(list(call.columns)[i]),
                                        dcc.Checklist(
                                            options=[{'label':ii,'value':jj} for ii,jj in zip(call.values[:,i],callRIC.values[:,i])],
                                            id='List-options-call'+str(i),className='radiobtn',
                                            values=[],labelStyle={'display': 'list-item'},
                                            )
                                ]
                                )
                        ]
        return html.Div(
                    dbc.Card(
                        dbc.CardBody([dbc.Row(html0)]),color="primary", outline=True,
                        ),
                    )
    else:
        return(' ')



@app.callback(
    dash.dependencies.Output('Options_Put_selection', 'children'),
    [dash.dependencies.Input('output-container-Filter', 'children')])
def GridOptions(children):
    if children!=None:
        # return str(children)
        putRIC=pd.DataFrame(json.loads(json.loads(str(children))['putRIC']))
        put=pd.DataFrame(json.loads(json.loads(str(children))['put']))

        html0=[]
        for i in range(len(put.columns)):
            html0=html0+[dbc.Col([
                                    html.P(list(put.columns)[i]),
                                        dcc.Checklist(
                                            options=[{'label':ii,'value':jj} for ii,jj in zip(put.values[:,i],putRIC.values[:,i])],
                                            id='List-options-put'+str(i), 
                                            values=[],labelStyle={'display': 'list-item'},
                                            )
                                ]
                                )
                        ]
        return html.Div(
                    dbc.Card(
                        dbc.CardBody([dbc.Row(html0)]),color="danger", outline=True,
                        ),
                )
    else:
        return(' ')



# @app.callback(
#     dash.dependencies.Output('table', 'data'),
#     [dash.dependencies.Input('table', 'data_timestamp')],
#     [dash.dependencies.State('table', 'data')],
# )
# def Calc0(timestamp, rows):
#     for row in rows:
#         try:
#             row['Position$*'] = float(row['Position$*']*row['TRDPRC_1*'])
#         except:
#             row['Position$*'] = 'NA'
#     return rows





@app.callback(
    dash.dependencies.Output('table', 'data'),
    # [dash.dependencies.Input('List-options-put'+str(i), 'values') for i in range(len(app.layout['output-container-DropD'].value))]+\
    # [dash.dependencies.Input('List-options-call'+str(i), 'values') for i in range(len(app.layout['output-container-DropD'].value))]
    [dash.dependencies.Input('List-options-call'+str(i), 'values') for i in range(3)]+\
    [dash.dependencies.Input('List-options-put'+str(i), 'values') for i in range(3)],
    [dash.dependencies.State('output-container-Chain', 'children')]
)
def CreatTabel(*op1):
    if op1!=None:
        children=list(op1)[-1]
        op1=list(op1)[:-1]
        optionsInfo_C=pd.DataFrame(json.loads(json.loads(str(children))['optionsInfo_C']))
        optionsInfo_P=pd.DataFrame(json.loads(json.loads(str(children))['optionsInfo_P']))
        optionsInfo=pd.DataFrame(json.loads(json.loads(str(children))['optionsInfo']))
        g=[]
        for x in (op1):
            g=g+x
        
        op1=g
        tab=optionsInfo[optionsInfo.Instrument.isin(op1)][['TRADE_DATE','TRDPRC_1',"PUTCALLIND","EXPIR_DATE","STRIKE_PRC"]]
        tab["Position*"]=0
        tab["Position$*"]=0
        # return (html.H4(str(list(op1))))
        return (tab.to_dict('records'))


@app.callback(
    dash.dependencies.Output('output-tabela-select', 'children'),
    # [dash.dependencies.Input('List-options-put'+str(i), 'values') for i in range(len(app.layout['output-container-DropD'].value))]+\
    # [dash.dependencies.Input('List-options-call'+str(i), 'values') for i in range(len(app.layout['output-container-DropD'].value))]
    # [dash.dependencies.Input('List-options-call'+str(i), 'values') for i in range(3)]+\
    # [dash.dependencies.Input('List-options-put'+str(i), 'values') for i in range(3)],
    [dash.dependencies.Input('output-container-DropD', 'children')]
)
def CreatTabel(op1):
    if op1!=None:
        ctx = dash.callback_context
        ctx_msg=json.dumps({
                            'states': ctx.states,
                            'triggered': ctx.triggered,
                            'inputs': ctx.inputs
                           })
        return (html.Pre(ctx))




# for i in range(10):
#     @app.callback(
#         dash.dependencies.Output('table', 'data'),
#         # [dash.dependencies.Input('List-options-put'+str(i), 'values') for i in range(len(app.layout['output-container-DropD'].value))]+\
#         # [dash.dependencies.Input('List-options-call'+str(i), 'values') for i in range(len(app.layout['output-container-DropD'].value))]
#         [dash.dependencies.Input('List-options-call'+str(i), 'values') for i in range(i)]+\
#         [dash.dependencies.Input('List-options-put'+str(i), 'values') for i in range(i)],
#         [dash.dependencies.State('output-container-Chain', 'children')]
#     )
#     def CreatTabel(*op1):
#         if op1!=None:
#             children=list(op1)[-1]
#             op1=list(op1)[:-1]
#             optionsInfo_C=pd.DataFrame(json.loads(json.loads(str(children))['optionsInfo_C']))
#             optionsInfo_P=pd.DataFrame(json.loads(json.loads(str(children))['optionsInfo_P']))
#             optionsInfo=pd.DataFrame(json.loads(json.loads(str(children))['optionsInfo']))
#             g=[]
#             for x in (op1):
#                 g=g+x
            
#             op1=g
#             tab=optionsInfo[optionsInfo.Instrument.isin(op1)][['TRADE_DATE','TRDPRC_1',"PUTCALLIND","EXPIR_DATE","STRIKE_PRC"]]
#             tab["Position*"]=0
#             tab["Position$*"]=0
#             # return (html.H4(str(list(op1))))
#             return (tab.to_dict('records'))





# @app.callback(
#     dash.dependencies.Output('output-tabela-select', 'children'),
#     # [dash.dependencies.Input('List-options-put'+str(i), 'values') for i in range(len(app.layout['output-container-DropD'].value))]+\
#     # [dash.dependencies.Input('List-options-call'+str(i), 'values') for i in range(len(app.layout['output-container-DropD'].value))]
#     [dash.dependencies.Input('List-options-call'+str(i), 'values') for i in range(int(3))]+\
#     [dash.dependencies.Input('List-options-put'+str(i), 'values') for i in range(int(3))]
# )
# def CreatTabel(*op1):
#     # return (html.H4(str(list(op1))))
#     return ([html.H4(str(list(op1))),
#             html.H4(
#                 str(
#                     # app.layout['output-date-len']
#                     )
#                 )
#             ])



# @app.callback(
#     dash.dependencies.Output('output-tabela-select', 'children'),
#     # [dash.dependencies.Input('List-options-put'+str(i), 'values') for i in range(len(app.layout['output-container-DropD'].value))]+\
#     # [dash.dependencies.Input('List-options-call'+str(i), 'values') for i in range(len(app.layout['output-container-DropD'].value))]
#     [dash.dependencies.Input('List-options-call'+str(i), 'values') for i in range(3)]+\
#     [dash.dependencies.Input('List-options-put'+str(i), 'values') for i in range(3)]
# )
# def CreatTabel(*op1):
#     # return (html.H4(str(list(op1))))
#     return ([html.H4(str(list(op1))),
            
#             html.H4(
#                 str(
#                     # (app.callback_map['Options_Call_selection.options'])
#                     )
#                 )
            
#             ])


    # # op1=list(op1)
    # optionsInfo_C=pd.DataFrame(json.loads(json.loads(children)['optionsInfo_C']))
    # optionsInfo_P=pd.DataFrame(json.loads(json.loads(children)['optionsInfo_P']))
    # # optionsInfo=pd.DataFrame(json.loads(json.loads(app.layout['output-container-Chain'].children)['optionsInfo']))
    # # optionsInfo=optionsInfo[optionsInfo.Instrument.isin(op1)]
    # return (html.Div(
    #         dt.DataTable(
    #             id="Op_strateg",
    #             columns=[{"name": i, "id": i} for i in optionsInfo.columns],
    #             data=optionsInfo.to_dict('records'),
    #             )

    #     ))

# @app.callback(
#     dash.dependencies.Output('Options_Put_selection', 'children'),
#     [dash.dependencies.Input('output-container-Filter', 'children')])
# def GridOptions(children):
    # putRIC=pd.DataFrame(json.loads(json.loads(children)['putRIC']))
    # put=pd.DataFrame(json.loads(json.loads(children)['put']))

#     html1=[]
#     for i in range(len(put.columns)):
#         html1=html1+[(html.Div(
#                         [html.P(list(put.columns)[i]),
#                             dcc.Checklist(
#                                 options=[{'label':ii,'value':jj} for ii,jj in zip(put.values[:,i],putRIC.values[:,i])],
#                                 id='List-options-put'+str(i), 
#                                 # values=put.values[:,i], #labelStyle={'display': 'inline-block'}
#                                 )
#                             ],className="two columns"))]

#     return html.Div(html1, className="row")


# @app.callback(
#     dash.dependencies.Output('Output-tabela-opicoes', 'children'),
#     # [dash.dependencies.Input('button10', 'n_clicks')],
#     [dash.dependencies.Input('List-options-put'+str(0), 'value')])#+
# #    [dash.dependencies.State('List-options-call'+str(i), 'value') for i in range(3)])
# def Criar_tavela(Values):
#    return str(Values)




# , className="row"
# @app.callback(
#     dash.dependencies.Output('output-container-teste', 'children'),
#     # [dash.dependencies.Input('button3', 'n_clicks')],
#     [dash.dependencies.State('output-container-Chain', 'children')])
# def FilDelta(n_clicks,children):
#     return(str(pd.DataFrame(json.loads(children['spot']))))
#     # optionsInfo_C=pd.DataFrame(json.loads(RE['optionsInfo_C']))
#     # optionsInfo_P=pd.DataFrame(json.loads(RE['optionsInfo_P']))
#     # Selec_C=Func.DeltaStreikFilter(optionsInfo_C,value[0],value[1])
#     # Selec_P=Func.DeltaStreikFilter(optionsInfo_P,value[0],value[1])
#     # callRIC=pd.DataFrame(Selec_C).T
#     # callRIC.columns=lldate
#     # call=pd.DataFrame([optionsInfo[optionsInfo.Instrument.isin(Selec_C[i])].STRIKE_PRC.values for i in range(len(Selec_C))]).T
#     # call.columns=lldate
#     # put=pd.DataFrame(Selec_P).T
#     # put.columns=lldate
#     # put=pd.DataFrame([optionsInfo[optionsInfo.Instrument.isin(Selec_P[i])].STRIKE_PRC.values for i in range(len(Selec_P))]).T
#     # put.columns=lldate

#     # return(str([callRIC,call],[putRIC,put]))

if __name__ == "__main__":
    app.run_server(debug=True)



