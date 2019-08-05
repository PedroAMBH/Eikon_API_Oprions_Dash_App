import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_core_components as dcc

app = dash.Dash(__name__, assets_external_path=[dbc.themes.BOOTSTRAP])
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
#                             assets_external_path=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True



app.layout = html.Div([
    html.H1('Smoothie Fixed Benefit Prices'),
    html.P("These prices are common for all routes in India."),
    html.P("Peak months are:-Jan,June, July, August, November, December."),
    html.P("Peak Hours ( During Peak Months ):-9 A.M. to Midnight"),
    html.P("Peak Hours ( During Non Peak Months ):-12 P.M. - 12 A.M."),
    html.H3('Select Airline'),
    dcc.Dropdown(
        id='datasource-1',
        options=[
            {'label': i, 'value': i} for i in ['Low Delay Airlines (6E, UK)','High Delay Airlines (9W,AI,SG,G8)']
        ],
    ),
    html.H3('Select Peak/Non-Peak Month'),
    dcc.Dropdown(
        id='datasource-2',
        options=[
            {'label': i, 'value': i} for i in ['Peak Month','Non Peak Month']
        ]

    ),   
    html.Hr(),
    html.Div('Select Peak/Non Peak Hour and Threshold Delay'),
    html.Div(
        id='controls-container'
    ),
    html.Hr(),
    html.Div('Output'),
    html.Div(
        id='output-container'
    )
])


def generate_control_id(value):
    return 'Control {}'.format(value)

DYNAMIC_CONTROLS = {
    'Low Delay Airlines (6E, UK)': dcc.Dropdown(
        id=generate_control_id('Low Delay Airlines (6E, UK)'),
        options=[{'label': '{}'.format(i), 'value': i} for i in list(price['Hour Peaks'][price['Airlines']=='Low Delay Airlines (6E, UK)'].unique())]
    ),
    'High Delay Airlines (9W,AI,SG,G8)': dcc.Dropdown(
        id=generate_control_id('High Delay Airlines (9W,AI,SG,G8)'),
        options=[{'label': '{}'.format(i), 'value': i} for i in list(price['Hour Peaks'][price['Airlines']=='High Delay Airlines (9W,AI,SG,G8)'].unique())]
    ),
    'Peak Month': dcc.Dropdown(
        id=generate_control_id('Peak Month'),
        options=[{'label': '{}'.format(i), 'value': i} for i in [60,90,120,150,180]]
    ),
    'Non Peak Month': dcc.Dropdown(
        id=generate_control_id('Non Peak Month'),
        options=[{'label': '{}'.format(i), 'value': i} for i in [60,90,120,150,180]]
    )
}

@app.callback(
    Output('controls-container', 'children'),
    [Input('datasource-1', 'value'),
     Input('datasource-2', 'value')])
def display_controls(datasource_1_value, datasource_2_value):
    # generate 2 dynamic controls based off of the datasource selections
    return html.Div([
        DYNAMIC_CONTROLS[datasource_1_value],
        DYNAMIC_CONTROLS[datasource_2_value],
    ])

def generate_output_id(value1, value2):
    return '{} {} container'.format(value1, value2)

@app.callback(
    Output('output-container', 'children'),
    [Input('datasource-1', 'value'),
     Input('datasource-2', 'value')])
def display_controls(datasource_1_value, datasource_2_value):
    # create a unique output container for each pair of dyanmic controls
    return html.Div(id=generate_output_id(
        datasource_1_value,
        datasource_2_value
    ))
def prem(a,b,c,d):
    return (price['Office Premium ( INR )'][(price['Hour Peaks']==a)&(price['Threshold Delay ( Min )']==b)&(price['Airlines']==c)&(price['Month Peaks']==d)])
def incidence(a,b,c,d):
    return (price['Incidence Rate (%)'][(price['Hour Peaks']==a)&(price['Threshold Delay ( Min )']==b)&(price['Airlines']==c)&(price['Month Peaks']==d)])

def generate_output_callback(datasource_1_value, datasource_2_value):
    def output_callback(control_1_value, control_2_value):
        # This function can display different outputs depending on
        # the values of the dynamic controls
        premium=prem(control_1_value,control_2_value,datasource_1_value,datasource_2_value)
        incidence_rate=incidence(control_1_value,control_2_value,datasource_1_value,datasource_2_value)
        return '''
            For the selected values, premium in INR is {} and incidence rate is {} %
        '''.format(
            list(premium)[0],
            list(incidence_rate)[0]
            )
    return output_callback

app.config.supress_callback_exceptions = True

# create a callback for all possible combinations of dynamic controls
# each unique dynamic control pairing is linked to a dynamic output component
for value1, value2 in itertools.product(
        [o['value'] for o in app.layout['datasource-1'].options],
        [o['value'] for o in app.layout['datasource-2'].options]):
    app.callback(
        Output(generate_output_id(value1, value2), 'children'),
        [Input(generate_control_id(value1), 'value'),
         Input(generate_control_id(value2), 'value')])(
        generate_output_callback(value1, value2)
    )



# if __name__ == '__main__':
#     application.run(port=8080)



app = dash.Dash(__name__, assets_external_path=[dbc.themes.BOOTSTRAP])
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
#                             assets_external_path=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True

# app.layout = html.Div([collapse])


# @app.callback(
#     Output("ret", "children"),
#     [Input("collapse-button", "values")],
# )
# def toggle_collapse(is_open):
#     return html.H2(str(is_open))







if __name__ == "__main__":
    app.run_server()