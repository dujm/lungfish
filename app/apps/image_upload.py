import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H3('Image Upload'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'Select Dataset - {}'.format(i), 'value': i} for i in [
                'Sample Dataset'
                ]
            ]
        
    ),
    html.Div(id='app-3-display-value'),
    dcc.Link('Go to Image Assets', href='/apps/image_assets')
])


@app.callback(
    Output('app-3-display-value', 'children'),
    [Input('app-3-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
