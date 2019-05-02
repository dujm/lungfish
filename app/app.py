<<<<<<< HEAD
import os, numpy as np, pandas as pd

from functools import partial
from collections import defaultdict

# flask
from flask import Flask, send_from_directory
from flask_cors import CORS

=======
################################################################################
# Import packages
################################################################################
import os, numpy as np, pandas as pd

>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
# packages for visualization
import pydicom
import plotly.graph_objs as go

# dash
import flask
import dash
<<<<<<< HEAD

import dash_table_experiments as dt
=======
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
import dash_html_components as html


import base64
from urllib.parse import quote as urlquote


################################################################################

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

##

app.config.suppress_callback_exceptions = True
<<<<<<< HEAD
app.scripts.config.serve_locally = True
colors = {'background': '#FFFFFF', 'text': '#111111', 'table': '#111111'}
app.title = 'X-Ray Vision'

################################################################################

################################################################################


=======
colors = {"background": "#FFFFFF", "text": "#111111", "table": "#111111"}
app.title = "X-Ray Vision"
################################################################################
# Functions used in the app
################################################################################
# Count by columns in dataframe
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
def count_by_col(df, colname, new_colname):
    df_count_by_colname = df.groupby([colname]).size().reset_index(name=new_colname)
    df.rename(index=str, columns={"A": "Group", "B": "c"})
    return df_count_by_colname


# Count by 2 columns in dataframe
def count_two_cols(df, col1, col2, new_colname):
    df_count_by_colname = df.groupby([col1, col2]).size().reset_index(name=new_colname)
<<<<<<< HEAD
    df_count_by_colname.rename(columns={col1: 'Group'}, inplace=True)
=======
    df_count_by_colname.rename(columns={col1: "Group"}, inplace=True)
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
    return df_count_by_colname


# Count by patient age ranges
def count_by_PatientAge(df, col2, new_colname):
    from itertools import cycle

    # Age ranges
    ranges = [0, 20, 40, 60, 100]
    df_count = (
        df.groupby([col2, pd.cut(df.PatientAge, ranges)])
        .size()
        .reset_index(name=new_colname)
    )
    # Add column age_group based on ranges
<<<<<<< HEAD
    age_group = cycle(['Age 0-20', 'Age 20-40', 'Age 40-60', 'Age 60-80'])
    df_count['Group'] = [next(age_group) for age in range(len(df_count))]
    df_count_age_col2 = df_count.drop(['PatientAge'], axis=1)
=======
    age_group = cycle(["Age 0-20", "Age 20-40", "Age 40-60", "Age 60-80"])
    df_count["Group"] = [next(age_group) for age in range(len(df_count))]
    df_count_age_col2 = df_count.drop(["PatientAge"], axis=1)
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
    return df_count_age_col2


# Return indicator div
def indicator(color, text, id_value):
    return html.Div(
        [
            html.P(text, className="twelve columns indicator_text"),
            html.P(id=id_value, className="indicator_value"),
        ],
        className="four columns indicator",
    )


pl_bone = [
<<<<<<< HEAD
    [0.0, 'rgb(0, 0, 0)'],
    [0.05, 'rgb(10, 10, 14)'],
    [0.1, 'rgb(21, 21, 30)'],
    [0.15, 'rgb(33, 33, 46)'],
    [0.2, 'rgb(44, 44, 62)'],
    [0.25, 'rgb(56, 55, 77)'],
    [0.3, 'rgb(66, 66, 92)'],
    [0.35, 'rgb(77, 77, 108)'],
    [0.4, 'rgb(89, 92, 121)'],
    [0.45, 'rgb(100, 107, 132)'],
    [0.5, 'rgb(112, 123, 143)'],
    [0.55, 'rgb(122, 137, 154)'],
    [0.6, 'rgb(133, 153, 165)'],
    [0.65, 'rgb(145, 169, 177)'],
    [0.7, 'rgb(156, 184, 188)'],
    [0.75, 'rgb(168, 199, 199)'],
    [0.8, 'rgb(185, 210, 210)'],
    [0.85, 'rgb(203, 221, 221)'],
    [0.9, 'rgb(220, 233, 233)'],
    [0.95, 'rgb(238, 244, 244)'],
    [1.0, 'rgb(255, 255, 255)'],
=======
    [0.0, "rgb(0, 0, 0)"],
    [0.05, "rgb(10, 10, 14)"],
    [0.1, "rgb(21, 21, 30)"],
    [0.15, "rgb(33, 33, 46)"],
    [0.2, "rgb(44, 44, 62)"],
    [0.25, "rgb(56, 55, 77)"],
    [0.3, "rgb(66, 66, 92)"],
    [0.35, "rgb(77, 77, 108)"],
    [0.4, "rgb(89, 92, 121)"],
    [0.45, "rgb(100, 107, 132)"],
    [0.5, "rgb(112, 123, 143)"],
    [0.55, "rgb(122, 137, 154)"],
    [0.6, "rgb(133, 153, 165)"],
    [0.65, "rgb(145, 169, 177)"],
    [0.7, "rgb(156, 184, 188)"],
    [0.75, "rgb(168, 199, 199)"],
    [0.8, "rgb(185, 210, 210)"],
    [0.85, "rgb(203, 221, 221)"],
    [0.9, "rgb(220, 233, 233)"],
    [0.95, "rgb(238, 244, 244)"],
    [1.0, "rgb(255, 255, 255)"],
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
]


def histogram_equalization(img, no_bins):

    # img- the image as a numpy.array
    # the appropriate number of bins, `no_bins` in the histogram is chosen by experiments,
    # until the contrast is convenient

    image_hist, bins = np.histogram(img.flatten(), no_bins, normed=True)
    csum = image_hist.cumsum()
    cdf_mult = np.max(img) * csum / csum[-1]  # cdf multiplied by a factor

    #  linear interpolation of cdf_mult to get new pixel values
    im_new = np.interp(img.flatten(), bins[:-1], cdf_mult)

    return im_new.reshape(img.shape), cdf_mult


## Parse data
def parse_dcm_metadata(dcm):
    """author kaggle/jtlowery"""
    unpacked_data = {}
    group_elem_to_keywords = {}
    # iterating here to force conversion from lazy RawDataElement to DataElement
    for d in dcm:
        pass
    # keys are pydicom.tag.BaseTag, values are pydicom.dataelem.DataElement
    for tag, elem in dcm.items():
        tag_group = tag.group
        tag_elem = tag.elem
        keyword = elem.keyword
        group_elem_to_keywords[(tag_group, tag_elem)] = keyword
        value = elem.value
        unpacked_data[keyword] = value
    return unpacked_data, group_elem_to_keywords


# A function to read dcm meta data into a dataframe
def read_dcm_meta(image_directory, save_csv_dir):
    image_fps = []
    for (dirpath, dirnames, filenames) in os.walk(image_directory):
        # print(filenames)
        image_fps += [
<<<<<<< HEAD
            os.path.join(dirpath, file) for file in filenames if file.endswith('.dcm')
        ]
    # print(len(image_fps), '.dcm files were found in', image_directory)
=======
            os.path.join(dirpath, file) for file in filenames if file.endswith(".dcm")
        ]
    print(len(image_fps), ".dcm files were found in", image_directory)
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3

    dcms = [pydicom.read_file(x, stop_before_pixels=True) for x in image_fps]

    meta, tag_to_key = zip(*[parse_dcm_metadata(x) for x in dcms])

    df_dcm = pd.DataFrame.from_records(data=meta)
<<<<<<< HEAD
    # print(df_dcm.head(1))
    filename = 'df_dcm_metadata_extraction.csv'
=======
    print(df_dcm.head(1))
    filename = "df_dcm_" + str(len(image_fps)) + "dash_sample.csv"
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
    df_dcm.to_csv(os.path.join(save_csv_dir, filename), index=False)
    return df_dcm


def get_pl_image(dicom_filename, hist_equal=False, no_bins=None):
    # dicom_filename- a string 'filename.dcm'
    # no_bins is the number of bins for histogram when hist_equal=False, else it is None
    # returns the np.array that defines the z-value for the heatmap representing the dicom image

<<<<<<< HEAD
    dic_file = pydicom.read_file(dicom_filename)  # force=True
=======
    dic_file = pydicom.read_file(dicom_filename)
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
    img = dic_file.pixel_array  # get the image as a numpy.array
    if hist_equal and isinstance(no_bins, int):
        img_new = histogram_equalization(img, no_bins)[0]
        img_new = np.array(img_new, dtype=np.int16)
        return np.flipud(img_new)
    else:
        return np.flipud(img)


# Show DICOM image heatmap WITH bounding box annotaion
def DICOM_heatmap(z, title, x0, x1, y0, y1, width=600, height=600, colorscale=pl_bone):

    trace0 = dict(
<<<<<<< HEAD
        type='heatmap',
        z=z,
        colorscale=colorscale,
        zsmooth='best',
=======
        type="heatmap",
        z=z,
        colorscale=colorscale,
        zsmooth="best",
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
        colorbar=dict(thickness=20, ticklen=4),
    )

    trace1 = go.Scatter(
        x=[x1, x1],
        y=[y0, y1],
<<<<<<< HEAD
        mode='lines',
        line=dict(color=('rgb(252,141,89)'), width=2),
=======
        mode="lines",
        line=dict(color=("rgb(252,141,89)"), width=2),
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
        showlegend=False,
    )
    trace2 = go.Scatter(
        x=[x0, x0],
        y=[y0, y1],
<<<<<<< HEAD
        mode='lines',
        line=dict(color=('rgb(252,141,89)'), width=2),
=======
        mode="lines",
        line=dict(color=("rgb(252,141,89)"), width=2),
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
        showlegend=False,
    )
    trace3 = go.Scatter(
        x=[x0, x1],
        y=[y0, y0],
<<<<<<< HEAD
        mode='lines',
        line=dict(color=('rgb(252,141,89)'), width=2),
=======
        mode="lines",
        line=dict(color=("rgb(252,141,89)"), width=2),
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
        showlegend=False,
    )
    trace4 = go.Scatter(
        x=[x0, x1],
        y=[y1, y1],
<<<<<<< HEAD
        mode='lines',
        line=dict(color=('rgb(252,141,89)'), width=2),
        showlegend=False,
    )

    data = [trace0, trace1, trace2, trace3, trace4]
    axis = dict(zeroline=False, showgrid=True, ticklen=4)
    layout = dict(
        width=600,
        height=600,
        font=dict(family='Balto', size=12),
        xaxis=dict(axis),
        yaxis=dict(axis),
        title=title,
    )

=======
        mode="lines",
        line=dict(color=("rgb(252,141,89)"), width=2),
        showlegend=False,
    )

    data = [trace0, trace1, trace2, trace3, trace4]
    axis = dict(zeroline=False, showgrid=True, ticklen=4)
    layout = dict(
        width=600,
        height=600,
        font=dict(family="Balto", size=12),
        xaxis=dict(axis),
        yaxis=dict(axis),
        title=title,
    )

>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
    return dict(data=data, layout=layout, axis=axis)  #


# Show DICOM image heatmap without bounding box annotaion
def DICOM_heatmap2(z, title, width=600, height=600, colorscale=pl_bone):

    data = [
        dict(
<<<<<<< HEAD
            type='heatmap',
            z=z,
            colorscale=colorscale,
            zsmooth='best',
=======
            type="heatmap",
            z=z,
            colorscale=colorscale,
            zsmooth="best",
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
            colorbar=dict(thickness=20, ticklen=4),
        )
    ]

    axis = dict(zeroline=False, showgrid=False, ticklen=4)
    layout = dict(
        width=600,
        height=600,
<<<<<<< HEAD
        font=dict(family='Balto', size=12),
=======
        font=dict(family="Balto", size=12),
>>>>>>> a6178f65863b38ebaaa1b989bd6eb767ecf162e3
        xaxis=dict(axis),
        yaxis=dict(axis),
        title=title,
    )

    return dict(data=data, layout=layout, axis=axis)  #


def df_to_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])]
        +
        # Body
        [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ]
    )
