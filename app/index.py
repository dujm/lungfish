# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import flask
import plotly.plotly as py
from plotly import graph_objs as go
import math

from apps import image_assets,image_summary, image_upload
from app import app, server,indicator
# Add this for horuku 
server = app.server
app.layout = html.Div(
    [
        # header
        html.Div([
            html.Div(
                html.Img(src='https://raw.githubusercontent.com/oceanprotocol/art/master/logo/logo-white.png',height="90%")
                ,style={"float":"right","height":"100%"}),
            html.H3("X-Ray Vision", className='app-title'),


            ],
            className="row header"
),


        # tabs
        html.Div([
            dcc.Tabs(
                id="tabs",
                style={"height":"60","verticalAlign":"middle", 'fontSize': 22},
                children=[
                    dcc.Tab(label="Image Asset Visualisation", value="image_assets_tab"),
                    dcc.Tab(label="Image Asset Summary", value="image_summary_tab"),
                    dcc.Tab(label="Local Image Processing", value="image_upload_tab")

                ],
                value="image_assets_tab",
            )

            ],
            className="row tabs_div"
            ),


        # divs that save dataframe for each tab
        html.Div(),
        html.Div(), # image_summary df
        html.Div(), # image_upload df



        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "5% 10%"}),


        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)


@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "image_assets_tab":
        return image_assets.layout
    elif tab == "image_summary_tab":
        return image_summary.layout
    elif tab == "image_upload_tab":
        return image_upload.layout
    else:
        return image_assets.layout


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
