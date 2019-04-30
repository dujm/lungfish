################################################################################
# Import packages
################################################################################
import os, urllib, pandas as pd


# dash
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table_experiments as dt
import dash_html_components as html


# import functions from app.py
from app import app, server, pl_bone, colors, indicator, get_pl_image, DICOM_heatmap

################################################################################
# Directories
################################################################################
# Sample image data
sample_image = "./data/sample_image/"

# Sample meta data
sample_meta = "./data/sample_meta/"

################################################################################
# Data
################################################################################
df1 = pd.read_csv(
    "./data/sample_meta/df_dcm_merge_box_bbcounts_app1000samples_cleaned.csv"
)
df1["Number"] = range(1, len(df1) + 1)

dataframes = {"Sample dataset": df1}

################################################################################
# App Layout
################################################################################
layout = [
    # 1. Dropdown
    html.Div(
        [
            html.H3("Visualization of Registered Medical Images"),
            dcc.Dropdown(
                id="app1dropdown",
                options=[{"label": df, "value": df} for df in dataframes],
                value="Sample dataset",
            ),
        ],
        className="row",
        style={"marginBottom": 5, "marginTop": 50, "fontsize": 20},
    ),
    # 2. Indicators
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
    ################################################################################
    # 3. Table
    html.Div(
        style={"backgroundColor": colors["background"], "color": colors["text"]},
        children=[
            html.H3("Metadata of DICOM Files"),
            # use datatable experiments dt
            dt.DataTable(
                id="dt_interactive",
                # rows
                rows=df1.to_dict("records"),  # initialize the rows
                columns=df1.columns,
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
            html.H2(),
            html.A(
                "Download Data",
                id="download-link",
                download="DICOM_1000_image_assets.csv",
                href="",
                target="_blank",
            ),
            html.Hr(),
            html.H2("Image Visualization of DICOM Files"),
            html.Div(
                id="selected-indexes", style={"margin-top": 50, "marginBottom": 10}
            ),
            dcc.Graph(id="dt_graph"),
        ],
    ),
]

################################################################################
# Callbacks
################################################################################
# 1. Update dt.DataTable rows in a callback
@app.callback(
    Output("dt_interactive", "selected_row_indices"),
    [Input("dt_graph", "clickData")],
    [State("dt_interactive", "selected_row_indices")],
)
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData["points"]:
            if point["pointNumber"] in selected_row_indices:
                selected_row_indices.remove(point["pointNumber"])
            else:
                selected_row_indices.append(point["pointNumber"])
                print("selected_row_indices", selected_row_indices)
    return selected_row_indices


################################################################################
# 2. Download table link
@app.callback(
    dash.dependencies.Output("download-link", "href"),
    [dash.dependencies.Input("dt_interactive", "rows")],
)
def update_download_link(rows):
    dff = pd.DataFrame(rows)
    txt_string = dff.to_csv(index=False, header=True, encoding="ascii")
    txt_string = "data:text/csv;ascii," + urllib.parse.quote(txt_string)
    return txt_string


################################################################################
# 3. Update dcm visulization graph
@app.callback(
    Output("dt_graph", "figure"),
    [Input("dt_interactive", "rows"), Input("dt_interactive", "selected_row_indices")],
)
def update_figure(rows, selected_row_indices):
    # df1 = pd.DataFrame(rows)
    selected_rows = [rows[i] for i in selected_row_indices]
    # selected_rows=selected_row_indices[-1]
    print(selected_rows)
    print(len(selected_rows))
    newst_row = selected_rows[0]
    print("the new one is", selected_rows[0])
    # limit to one image
    # 1) Select image name
    # image_dcm = [y['image_dcm'] for y in selected_rows]
    newest_image_dcm = newst_row["image_dcm"]
    # print('the neweste image_dcm is',newest_image_dcm)
    newset_image_name = "".join(map(str, newest_image_dcm))
    # print('newset_image_name', newset_image_name)

    # 2) Aad rectangle on the plot to show opacity regions
    if newst_row["x"] is not None:
        x0, y0 = newst_row["x"], newst_row["y"]
        width, height = newst_row["width"], newst_row["height"]
        x1 = x0 + width
        y1 = y0 + height
    else:
        x0, x1, y0, y1 = 0, 0, 0, 0
    # 3) Plot heatmap
    pl_img = get_pl_image(
        os.path.join(sample_image, newset_image_name), hist_equal=True, no_bins=36
    )
    fig = DICOM_heatmap(
        pl_img,
        str(newset_image_name),
        x0,
        x1,
        y0,
        y1,
        width=600,
        height=600,
        colorscale=pl_bone,
    )

    return fig


################################################################################
################################################################################
