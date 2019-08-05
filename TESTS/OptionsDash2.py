# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:16:29 2019

@author: U6035631
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app = dash.Dash()
app.config.suppress_callback_exceptions = True


app.layout = html.Div(children=[
    html.H1(children='Dash Tutorials'),
    dbc.Button('Submit', 
            id='button0',
            color="primary"),
    dcc.Graph(
        id='example',animate=True,
    )
])
app.config.suppress_callback_exceptions = True

@app.callback(
    dash.dependencies.Output('example', 'figure'),
    [dash.dependencies.Input('button0', 'n_clicks')],
)
def up(n_clicks):
    if n_clicks!=None:
        figure={'data': [go.Scatter(
                            x= [1, 2, 3, 4, 5],
                            y=[9, 6, 2, 1, 5],
                            mode='lines')],
               'layout': {'title': 'Basic Dash Example'}
                }
        print(figure)

        return ({'data': [go.Scatter(
                            x= [1, 2, 3, 4, 5],
                            y=[9, 6, 2, 1, 5],
                            mode='lines')],
               'layout': {'title': 'Basic Dash Example'}
                })
    else:
        return ({'data': [go.Scatter(
                            x= [0],
                            y=[0],
                            mode='lines')],
               'layout': {'title': 'Basic Dash Example'}
                })




if __name__ == '__main__':
    app.run_server(debug=True)


