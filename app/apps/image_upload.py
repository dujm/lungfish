################################################################################
# Import packages
################################################################################
import os,  pandas as pd

# packages for visualization
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import plotly

# dash
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output,State
import dash_table_experiments as dt
import dash_html_components as html


# import functions from app.py
from app import app, server, colors, parse_dcm_metadata, read_dcm_meta,  get_pl_image, DICOM_heatmap, DICOM_heatmap2

#pl_bone, colors,df_to_table, histogram_equalization,

################################################################################
# Functions
################################################################################


################################################################################
# Directories
################################################################################
# Copy your images here
local_image=('./data/local_image/')

# Copy your meta data here
local_meta=('./data/local_meta/')

################################################################################
# Data
################################################################################
# 1.1 Read DICOM images and summarize meta data into a csv file
read_df =read_dcm_meta(local_image,local_meta)

# Read the meta data csv file
df =pd.read_csv(os.path.join(local_meta,'df_dcm_dash_local.csv'))
print('local',df.head(2))

dataframes = {'Local medical images': df}
################################################################################
# App Layout
################################################################################
layout = [
    # top controls
    html.Div(
        [
        html.H3("Local Medical Images"),
        dcc.Dropdown(
            id='app3dropdown',
            options=[{'label': df, 'value': df} for df in dataframes],
            value ='Local medical images')],
            className="row",
            style={'marginBottom': 5, 'marginTop': 50,'fontsize':20}),

        # 2. 2nd row: table
    html.Div(
        style={'backgroundColor': colors['background'],'color': colors['text']},
        children =
        [
            html.H3('Metadata of DICOM Files'),
        # use datatable experiments dt
            dt.DataTable(
            id='dt_interactive_local',
            # rows
            rows=df.to_dict('records'),# initialize the rows
            columns=df.columns,
            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[0],
            max_rows_in_viewport=10,
            resizable =True,
            enable_drag_and_drop=True,
            header_row_height=50,
            column_widths=200,
            row_scroll_timeout=1,
            row_update= True,
            editable =True
            ),
            html.H2(''),
            html.H2('Image Visualization of DICOM Files'),
            html.Div(id='selected-indexes',style={'margin-top': 50,'marginBottom': 10}),
            dcc.Graph(id='dt_graph_local')
        ]
        ),

]


################################################################################
# Callbacks
################################################################################
# 1. Update dt.DataTable rows in a callback
@app.callback(
    Output('dt_interactive_local', 'selected_row_indices'),
    [Input('dt_graph_local', 'clickData')],
    [State('dt_interactive_local', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
                print('selected_row_indices',selected_row_indices)
    return selected_row_indices

################################################################################
# 1.2 update dt.graph
@app.callback(
    Output('dt_graph_local', 'figure'),
    [Input('dt_interactive_local', 'rows'),
     Input('dt_interactive_local', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    #df = pd.DataFrame(rows)
    selected_rows=[rows[i] for i in selected_row_indices]
    #selected_rows=selected_row_indices[-1]
    print(selected_rows)
    print(len(selected_rows))
    newst_row = selected_rows[0]
    print('the new one is',selected_rows[0])
    # limit to one image
    # 1) Select image name
    #image_dcm = [y['image_dcm'] for y in selected_rows]
    newest_image_dcm = newst_row['image_dcm']
    #print('the neweste image_dcm is',newest_image_dcm)
    newset_image_name=''.join(map(str, newest_image_dcm))
    #print('newset_image_name', newset_image_name)
    pl_img=get_pl_image(os.path.join(local_image,newset_image_name), hist_equal=True, no_bins=36)

    fig=DICOM_heatmap2(pl_img, str(newset_image_name))
    #fig3 =py.iplot(fig2, filename='DICOM-MRBRAIN') don't do image show in dash
    # add patches

    return fig

################################################################################
################################################################################
