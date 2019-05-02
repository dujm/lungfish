################################################################################
# Import packages
################################################################################
import os, glob, urllib, pandas as pd

# packages for visualization
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import plotly

# dash
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table_experiments as dt
import dash_html_components as html
import dash_table

import base64
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
import shutil
import datetime

# import functions from app.py
from app import (
    app,
    server,
    colors,
    parse_dcm_metadata,
    read_dcm_meta,
    get_pl_image,
    DICOM_heatmap,
    DICOM_heatmap2,
)

# pl_bone, colors,df_to_table, histogram_equalization,

################################################################################
# Functions
################################################################################
def parse_contents(contents, filename, date):
    return html.Div(
        [
            html.H6(filename),
            # html.H6(datetime.datetime.fromtimestamp(date)),
            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.Img(src=contents),
            html.Hr(),
            # html.Div('Raw Content'),
            # html.Pre(contents[0:200] + '...', style={
            #'whiteSpace': 'pre-wrap',
            #'wordBreak': 'break-all'
            # })
        ]
    )


################################################################################
# Directories

################################################################################
# Copy your images here
local_image = './data/local_image/'

# The DICOM meta information will be saved here
local_meta = './data/local_meta/'


################################################################################
# Make sure no user's data is saved on the server
################################################################################


dir_name = "./project/app_uploaded_files"
files = os.listdir(dir_name)

for item in files:
    if item.endswith(".dcm"):
        os.remove(os.path.join(dir_name, item))
    if item.endswith(".csv"):
        os.remove(os.path.join(dir_name, item))

################################################################################
# Folder for saving data during image processing. Data will be deleted at the end of the session
UPLOAD_DIRECTORY = "./project/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


################################################################################
# Local Data
################################################################################
# 1.1 Read DICOM images and summarize meta data into a csv file in local_meta directory
write_dcm_meta = read_dcm_meta(local_image, local_meta)

# Read the meta data csv file
df = pd.read_csv(os.path.join(local_meta, 'df_dcm_metadata_extraction.csv'))
################################################################################
################################################################################
# App Layout
################################################################################
layout = [
    # top controls
    html.H3("Local Medical Image Processing"),
    html.Div(
        [
            ################################################################################
            # Radio items
            dcc.RadioItems(
                id='radioitem',
                options=[
                    {'label': 'Upload one DICOM file', 'value': 'Upload1'},
                    # {'label': 'Select a folder (<=12 DICOM files)', 'value': 'Upload9'},
                    {'label': 'On-premise run', 'value': 'local1'},
                ],
                value='Upload1',
            )
        ],
        className="row",
        style={'marginBottom': 5, 'marginTop': 50, 'fontsize': 25}
        #'backgroundColor': colors['background'], 'color': colors['text']
    ),
    html.H2(''),
    html.Hr(),
    html.Div(id='display-selected-values'),
    html.Hr(),
]


################################################################################
# Callback 1 :Radio buttons
################################################################################
@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('radioitem', 'value')],
)
def update_radio(radioitem):
    if radioitem == 'Upload1':
        return html.Div(
            [  #
                html.H4('Processing your uploaded DICOM file'),
                html.Div(
                    style={
                        'backgroundColor': colors['background'],
                        'color': colors['text'],
                    },
                    children=[
                        html.H5("Upload a DICOM file"),
                        html.H2(''),
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div(
                                ["Drag and drop or click to select a file to upload."]
                            ),
                            style={
                                "width": "50%",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px",
                            },
                            multiple=True,  # TRUE
                        ),
                        # html.H5("Uploaded file list"),
                        # html.Ul(id="file-list"),
                        html.Div(id='output-image-upload'),
                        dcc.Graph(id='dt_graph_upload2'),
                        html.A(
                            'Download meta data (For all dcm files you have uploaded in this session)',
                            id='download-link2',
                            download="Metadata_extracted_from_dcm.csv",
                            href="",
                            target="_blank",
                        ),
                        html.H2(''),
                        html.H6('Note: No data is stored in the server'),
                    ],
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H4('Processing local DICOM files in ./app/data/local_image/'),
                html.H2(''),
                html.Div(
                    style={
                        'backgroundColor': colors['background'],
                        'color': colors['text'],
                    },
                    children=[
                        html.H4('Metadata extracted from DICOM Files'),
                        # use datatable experiments dt
                        dt.DataTable(
                            id='dt_interactive_local',
                            # rows
                            rows=df.to_dict('records'),  # initialize the rows
                            columns=df.columns,
                            row_selectable=True,
                            filterable=True,
                            sortable=True,
                            selected_row_indices=[0],
                            max_rows_in_viewport=10,
                            resizable=True,
                            enable_drag_and_drop=True,
                            header_row_height=50,
                            column_widths=200,
                            row_scroll_timeout=1,
                            row_update=True,
                            editable=True,
                        ),
                        html.H2(''),
                        html.H4('Image Visualization of DICOM Files'),
                        html.Div(
                            id='selected-indexes',
                            style={'margin-top': 50, 'marginBottom': 10},
                        ),
                        dcc.Graph(id='dt_graph_local'),
                    ],
                ),
            ],
            className='row',
        )


################################################################################
# Callback 2 :upload image
################################################################################
# Function to read uploaded image data


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]


###############################################################################
# Visualization of uploaded DICOM file
@app.callback(
    Output("dt_graph_upload2", "figure"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)
            read_dcm_meta(UPLOAD_DIRECTORY, UPLOAD_DIRECTORY)
            print('name is', name)
            if name.endswith('.dcm'):
                uploaded_image_name = ''.join(map(str, name))

                print(uploaded_image_name)
                pl_img2 = get_pl_image(
                    os.path.join(UPLOAD_DIRECTORY, uploaded_image_name),
                    hist_equal=True,
                    no_bins=36,
                )
                fig2 = DICOM_heatmap2(pl_img2, str(uploaded_image_name))

                return fig2


# Added on 22:09
#############################################
@app.callback(
    dash.dependencies.Output('download-link2', 'href'),
    [dash.dependencies.Input("dt_graph_upload2", "figure")],
)
def update_download_link2(df_upload):
    df_upload = pd.read_csv(
        os.path.join(UPLOAD_DIRECTORY, 'df_dcm_metadata_extraction.csv')
    )
    txt_string = df_upload.to_csv(index=False, header=True, encoding='ascii')
    txt_string = "data:text/csv;ascii," + urllib.parse.quote(txt_string)
    return txt_string


################################################################################
# Callback 3. Update dt.DataTable rows
################################################################################
@app.callback(
    Output('dt_interactive_local', 'selected_row_indices'),
    [Input('dt_graph_local', 'clickData')],
    [State('dt_interactive_local', 'selected_row_indices')],
)
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
                # print('selected_row_indices', selected_row_indices)
    return selected_row_indices


################################################################################
# 3.2 update dt.graph
@app.callback(
    Output('dt_graph_local', 'figure'),
    [
        Input('dt_interactive_local', 'rows'),
        Input('dt_interactive_local', 'selected_row_indices'),
    ],
)
def update_figure(rows, selected_row_indices):
    # df = pd.DataFrame(rows)
    selected_rows = [rows[i] for i in selected_row_indices]
    # selected_rows=selected_row_indices[-1]
    # print(selected_rows)
    # print(len(selected_rows))
    newst_row = selected_rows[0]
    # print('the new one is', selected_rows[0])
    # limit to one image
    # 1) Select image name
    # image_dcm = [y['image_dcm'] for y in selected_rows]
    newest_image_id = newst_row['PatientID']
    # print('the neweste image_dcm is',newest_image_dcm)
    newset_image_name = ''.join(map(str, newest_image_id)) + '.dcm'
    # print('newset_image_name', newset_image_name)
    pl_img = get_pl_image(
        os.path.join(local_image, newset_image_name), hist_equal=True, no_bins=36
    )

    fig = DICOM_heatmap2(pl_img, str(newset_image_name))
    # fig3 =py.iplot(fig2, filename='DICOM-MRBRAIN') don't do image show in dash
    # add patches

    return fig


################################################################################
# Clean user's data
# shutil.rmtree('./project/app_uploaded_files/')

################################################################################
dir_name = "./project/app_uploaded_files"
files = os.listdir(dir_name)

for item in files:
    if item.endswith(".dcm"):
        os.remove(os.path.join(dir_name, item))
    if item.endswith(".csv"):
        os.remove(os.path.join(dir_name, item))
