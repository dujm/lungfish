
import os, glob, numpy as np, pandas as pd

from functools import partial
from collections import defaultdict
# flask
from flask import Flask
from flask_cors import CORS
# packages for visualization
import pydicom
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

#####################################################################
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True
colors = {'background': '#FFFFFF','text': '#111111','table':'#111111'}

#####################################################################




# 3. Define function
#returns top indicator div
def indicator(color, text, id_value):
    return html.Div(
        [

            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",

    )


pl_bone=[[0.0, 'rgb(0, 0, 0)'],
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
         [1.0, 'rgb(255, 255, 255)']]
def histogram_equalization(img, no_bins):

    #img- the image as a numpy.array
    #the appropriate number of bins, `no_bins` in the histogram is chosen by experiments,
    #until the contrast is convenient

    image_hist, bins = np.histogram(img.flatten(), no_bins, normed=True)
    csum = image_hist.cumsum()
    cdf_mult = np.max(img) * csum / csum[-1] # cdf multiplied by a factor

    #  linear interpolation of cdf_mult to get new pixel values
    im_new = np.interp(img.flatten(), bins[:-1],  cdf_mult)

    return im_new.reshape(img.shape), cdf_mult


## Parse data
def parse_dcm_metadata(dcm):
    '''author kaggle/jtlowery'''
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
def read_dcm_meta(image_directory,save_csv_dir):
    image_fps = []
    for (dirpath, dirnames, filenames) in os.walk(image_directory):
        #print(filenames)
        image_fps += [os.path.join(dirpath, file) for file in filenames if file.endswith('.dcm')]
    print(len(image_fps),'.dcm files were found in',image_directory)

    dcms = [pydicom.read_file(x, stop_before_pixels=True) for x in image_fps]

    meta, tag_to_key = zip(*[parse_dcm_metadata(x) for x in dcms])

    df_dcm = pd.DataFrame.from_records(data=meta)
    print(df_dcm.head(1))
    filename= 'df_dcm_' + str(len(image_fps)) + 'dash_sample.csv'
    df_dcm.to_csv(os.path.join(save_csv_dir,filename),index=False)
    return df_dcm
# return html Table with dataframe values

def get_pl_image(dicom_filename, hist_equal=False, no_bins=None):
    #dicom_filename- a string 'filename.dcm'
    #no_bins is the number of bins for histogram when hist_equal=False, else it is None
    #returns the np.array that defines the z-value for the heatmap representing the dicom image

    dic_file=pydicom.read_file(dicom_filename)
    img=dic_file.pixel_array#get the image as a numpy.array
    if hist_equal and isinstance(no_bins, int):
        img_new=histogram_equalization(img, no_bins)[0]
        img_new=np.array(img_new, dtype=np.int16)
        return np.flipud(img_new)
    else:
        return np.flipud(img)

def DICOM_heatmap(z, title, width=600, height=600, colorscale=pl_bone):

    data=[dict(type='heatmap',
           z=z,
           colorscale=colorscale,
           zsmooth='best',
           colorbar=dict(thickness=20, ticklen=4),
              )
         ]

    axis=dict(zeroline=False, showgrid=False, ticklen=4)
    layout=dict(width=600, height=600,
            font=dict(family='Balto', size=12),
            xaxis= dict(axis),
            yaxis= dict(axis),
            title= title
            )

    return  dict(data=data, layout=layout,axis=axis) # added axis =axis



def df_to_table(df):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +

        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col])
                    for col in df.columns
                ]
            )
            for i in range(len(df))
        ]
    )

def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    '''
    Save a figure as a URI
    :param in_fig:
    :return:
    '''
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode('ascii').replace('\n', '')
    return 'data:image/png;base64,{}'.format(encoded)
