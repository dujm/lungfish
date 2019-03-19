import os, glob, numpy as np, pandas as pd

from functools import partial
from collections import defaultdict
# flask
from flask import Flask
from flask_cors import CORS
# packages for visualization
import pydicom, matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot, plot
import plotly

# dash

import flask
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output,State
import dash_table_experiments as dt
import dash_html_components as html
import dash_table
# datatable filtering
import json

from app import app, server, pl_bone, colors,indicator,  df_to_table, histogram_equalization, get_pl_image, DICOM_heatmap, read_dcm_meta

#####################################################################
# 2. directories
# Sample image data
sample_image=('./data/sample_image/')
sample_train = ('./data/sample_image/sample_train/')
sample_validate = ('./data/sample_image/sample_validate/')
sample_test= ('./data/image_data/sample_image/sample_test/')

# Sample meta data
sample_meta=('./data/sample_meta/')
#####################################################################
# 1.1 Read csv data
df =pd.read_csv('./data/sample_meta/df_dcm_merge_box_bbcounts_app1000samples_cleaned.csv')
df['Number'] = range(1, len(df) + 1)

df_target_path = pd.read_csv('./data/sample_meta/df_dcm_merge_target_path_1000samples_addLungOpacity_col.csv')

df_count=df_target_path.groupby(['LungOpacity']).size().reset_index(name='total')
###
df_opacity =df_target_path[df_target_path.LungOpacity=='Opacity']
df_normal =df_target_path[df_target_path.LungOpacity=='Normal']


# Gender
df_count_gender=df_target_path.groupby(['PatientSex']).size().reset_index(name='total')
df_opacity_gender=df_opacity.groupby(['PatientSex']).size().reset_index(name='total')
df_normal_gender=df_normal.groupby(['PatientSex']).size().reset_index(name='total')

# View Position
df_count_ViewPosition=df_target_path.groupby(['ViewPosition']).size().reset_index(name='total')
df_opacity_ViewPosition=df_opacity.groupby(['ViewPosition']).size().reset_index(name='total')
df_normal_ViewPosition=df_normal.groupby(['ViewPosition']).size().reset_index(name='total')

# Age
ranges = [0,20,40,60,100]
df_age=df_target_path.groupby(pd.cut(df_target_path.PatientAge, ranges)).size().reset_index(name='total')

df_opacity_age=df_opacity.groupby(pd.cut(df_opacity.PatientAge, ranges)).size().reset_index(name='total')

df_normal_age=df_normal.groupby(pd.cut(df_normal.PatientAge, ranges)).size().reset_index(name='total')

from itertools import cycle

age_group = cycle(['Age 0-20','Age 20-40','Age 40-60','Age 60-80'])
df_age['age_group'] = [next(age_group) for age in range(len(df_age))]
df_opacity_age['age_group'] = [next(age_group) for age in range(len(df_opacity_age))]
df_normal_age['age_group'] = [next(age_group) for age in range(len(df_normal_age))]



layout = [
    # top controls
    html.Div(
        [
        html.H1("Summary of Image Assets"),
        dcc.Dropdown(
            id='app-1-dropdown',
            options=[
                {'label': 'Select Dataset - {}'.format(i), 'value': i} for i in [
                    'Sample Dataset'
                    ]
                ]
            ),
        ],
        className="row",
        style={'marginBottom': 5, 'marginTop': 50,'fontsize':20},
    ),

    # indicators div
    html.Div(
        [
            indicator(
                "#00cc96",
                html.H4("1000 Samples"),
                "left_image_upload_indicator",
            ),
            indicator(
                "#119DFF",
                html.H4("225 Pneumonia Samples "),
                "middle_image_upload_indicator",
            ),
            indicator(
                "#EF553B",
                html.H4("775 Normal Samples"),
                "right_image_upload_indicator",
            ),
        ],
        className="row",
    ),


        # 3. 3nd row: table
    #2.1 By sex
    html.Div(
        style={},
        children =
        [
            html.H3('Summary By Gender'),
        ]
        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                        id='bar-graph_total',
                        figure={
                        'data': [
                            {'x': df_count_gender['PatientSex'], 'y': df_count_gender['total'], 'type': 'bar', 'name': 'Sum','text':df_opacity_gender['total'],
                            'textposition':'auto',
                            'marker':dict(color='rgb(189,189,189)')},
                            ],
                        'layout': {
                            'title': 'Number of samples'
                            }
                               }
                        )
                    ],
                    className='four columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        dcc.Graph(
                        id='bar-graph_total2',
                        figure={
                        'data': [
                            {'x':df_opacity_gender['PatientSex'], 'y': df_opacity_gender['total'], 'type': 'bar', 'name': 'Sum',
                            'text':df_opacity_gender['total'],
                            'textposition':'auto',
                            'marker':dict(color='rgb(244,165,130)')},
                            ],
                        'layout': {
                            'title': 'Number of samples'
                            }
                               }
                        )
                    ],
                    className='four columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        dcc.Graph(
                        id='bar-graph_total3',
                        figure={
                        'data': [
                            {'x': df_normal_gender['PatientSex'], 'y': df_normal_gender['total'], 'type': 'bar', 'name': 'Sum',
                            'text':df_normal_gender['total'],
                            'textposition':'auto',
                            'marker':dict(color='rgb(146,197,222)')},
                            ],
                        'layout': {
                            'title': 'Number of samples'
                            }
                               }
                        )
                    ],
                    className='four columns',
                    style={'margin-top': '10'}
                ),
            ],
            className='row'
        ),
# ViewPosition
html.Div(
    style={},
    children =
    [
        html.H3('Summary By ViewPosition'),
    ]
    ),

    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                    id='bar-graph_total4',
                    figure={
                    'data': [
                        {'x': df_count_ViewPosition['ViewPosition'], 'y': df_count_ViewPosition['total'], 'type': 'bar', 'name': 'Sum','text':df_opacity_ViewPosition['total'],
                        'textposition':'auto',
                        'marker':dict(color='rgb(189,189,189)')},
                        ],
                    'layout': {
                        'title': 'Number of samples'
                        }
                           }
                    )
                ],
                className='four columns',
                style={'margin-top': '10'}
            ),
            html.Div(
                [
                    dcc.Graph(
                    id='bar-graph_total5',
                    figure={
                    'data': [
                        {'x':df_opacity_ViewPosition['ViewPosition'], 'y': df_opacity_ViewPosition['total'], 'type': 'bar', 'name': 'Sum',
                        'text':df_opacity_ViewPosition['total'],
                        'textposition':'auto',
                        'marker':dict(color='rgb(244,165,130)')},
                        ],
                    'layout': {
                        'title': 'Number of samples'
                        }
                           }
                    )
                ],
                className='four columns',
                style={'margin-top': '10'}
            ),
            html.Div(
                [
                    dcc.Graph(
                    id='bar-graph_total6',
                    figure={
                    'data': [
                        {'x': df_normal_ViewPosition['ViewPosition'], 'y': df_normal_ViewPosition['total'], 'type': 'bar', 'name': 'Sum',
                        'text':df_normal_ViewPosition['total'],
                        'textposition':'auto',
                        'marker':dict(color='rgb(146,197,222)')},
                        ],
                    'layout': {
                        'title': 'Number of samples'
                        }
                           }
                    )
                ],
                className='four columns',
                style={'margin-top': '10'}
            ),
        ],
        className='row'
    ),
# Age
html.Div(
    style={},
    children =
    [
        html.H3('Summary By PatientAge'),
    ]
    ),

    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                    id='bar-graph_total7',
                    figure={
                    'data': [
                        {'x': df_age['age_group'], 'y': df_age['total'], 'type': 'bar', 'name': 'Sum','text': df_age['total'],
                        'textposition':'auto',
                        'marker':dict(color='rgb(189,189,189)')},
                        ],
                    'layout': {
                        'title': 'Number of samples'
                        }
                           }
                    )
                ],
                className='four columns',
                style={'margin-top': '10'}
            ),
            html.Div(
                [
                    dcc.Graph(
                    id='bar-graph_total8',
                    figure={
                    'data': [
                        {'x':df_opacity_age['age_group'], 'y': df_opacity_age['total'], 'type': 'bar', 'name': 'Sum',
                        'text':df_opacity_age['total'],
                        'textposition':'auto',
                        'marker':dict(color='rgb(244,165,130)')},
                        ],
                    'layout': {
                        'title': 'Number of samples'
                        }
                           }
                    )
                ],
                className='four columns',
                style={'margin-top': '10'}
            ),
            html.Div(
                [
                    dcc.Graph(
                    id='bar-graph_total9',
                    figure={
                    'data': [
                        {'x': df_normal_age['age_group'], 'y': df_normal_age['total'], 'type': 'bar', 'name': 'Sum',
                        'text':df_normal_age['total'],
                        'textposition':'auto',
                        'marker':dict(color='rgb(146,197,222)')},
                        ],
                    'layout': {
                        'title': 'Number of samples'
                        }
                           }
                    )
                ],
                className='four columns',
                style={'margin-top': '10'}
            ),
        ],
        className='row'
    ),
]
