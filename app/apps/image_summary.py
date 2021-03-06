################################################################################
# Import packages
################################################################################
import os, pandas as pd, numpy as np

# packages for visualization
import pydicom
from PIL import Image

import plotly
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls

# dash
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table_experiments as dt
import dash_html_components as html


# import functions from app.py
from app import (
    pl_bone,
    df_to_table,
    histogram_equalization,
    get_pl_image,
    DICOM_heatmap,
)


# Import functions
from app import app, server, count_two_cols, count_by_PatientAge, colors, indicator

from functools import partial
from collections import defaultdict
import matplotlib

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import time, datetime

################################################################################
# Directories
################################################################################
# Sample image data
sample_image = './data/sample_image/'
# Sample meta data
sample_meta = './data/sample_meta/'

################################################################################
# Data
################################################################################
# Read meata data
df_target_path = pd.read_csv(
    './data/sample_meta/df_dcm_merge_target_path_1000samples_addLungOpacity_col.csv'
)
#######################################
# Count samples by groups
#######################################
# For graph
# Select by Gender
dc_gender_opacity = count_two_cols(df_target_path, 'PatientSex', 'LungOpacity', 'total')
#######################################
# Select by ViewPosition
#######################################
dc_ViewPosition_opacity = count_two_cols(
    df_target_path, 'ViewPosition', 'LungOpacity', 'total'
)
# Select by Age
dc_age_opacity = count_by_PatientAge(df_target_path, 'LungOpacity', 'total')
#######################################
# Make a dictionary of three dataframes for dcc.Dropdown
#######################################
dataframes = {
    'By Gender': dc_gender_opacity,
    'By View Position': dc_ViewPosition_opacity,
    'By Age': dc_age_opacity,
}
# print(dataframes.keys())

#
################################################################################
# App Layout
################################################################################
layout = [
    # top
    html.Div(
        [
            html.H3("Summary of Registered Medical Images"),
            dcc.Dropdown(
                id='app2dropdown',
                options=[{'label': df, 'value': df} for df in dataframes],
                value='By Gender',
            ),
        ],
        className="row",
        style={'marginBottom': 5, 'marginTop': 50, 'fontsize': 20},
    ),
    # Indicators div
    html.Div(
        [
            indicator(
                "#00cc96", html.H4("1000 Samples"), "left_image_upload_indicator"
            ),
            indicator(
                "#119DFF",
                html.H4("225 Pneumonia Samples "),
                "middle_image_upload_indicator",
            ),
            indicator(
                "#EF553B", html.H4("775 Normal Samples"), "right_image_upload_indicator"
            ),
        ],
        className="row",
    ),
    # Bar plots
    html.Div(
        [
            html.Div(
                [dcc.Graph(id='bar-graph')],
                className='columns',
                style={'margin-top': '10'},
            )
        ],
        className='row',
    ),
]
################################################################################
# App Callback
################################################################################
@app.callback(
    dash.dependencies.Output('bar-graph', 'figure'),
    [dash.dependencies.Input('app2dropdown', 'value')],
)
def update_graph(app2dropdown):
    if app2dropdown == 'By Gender':
        df_plot = dc_gender_opacity
    elif app2dropdown == 'By View Position':
        df_plot = dc_ViewPosition_opacity
    else:
        df_plot = dc_age_opacity

    df_normal = df_plot[df_plot['LungOpacity'] == 'Normal']
    df_opacity = df_plot[df_plot['LungOpacity'] == 'Opacity']
    trace1 = go.Bar(
        x=df_normal['Group'],
        y=df_normal['total'],
        text=df_normal['total'],
        textposition='auto',
        name='Normal',
    )

    trace2 = go.Bar(
        x=df_opacity['Group'],
        y=df_opacity['total'],
        text=df_opacity['total'],
        textposition='auto',
        name='Pneumonia',
    )

    return {'data': [trace1, trace2], 'layout': go.Layout(barmode='group')}
