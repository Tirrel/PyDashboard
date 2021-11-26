import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from App import app
from manage.TableManager import updateCellsAux, updateByFile
from util.Dictionaries import *
from util.Globals import *
from util.Identifiers import *
from util.Keys import *

TAG = "PageSingle."

# -------------------------------------------------------
# LAYOUT
# -------------------------------------------------------
layout = html.Div(
    style={
        'backgroundColor': COLOR_PURPLE_DARK
    },
    children=[
        dcc.Store(id=ID_LAYOUT_SINGLE),

        html.Div(
            [
                dcc.Dropdown(
                    id=ID_SELECT_SERIAL_NUMBER,
                    className='dropdown_class',
                    placeholder="Select a serial number",
                    multi=False,
                    style={
                        'backgroundColor': COLOR_PURPLE,
                        'vertical-align': ALIGN_TOP,
                        'display': INLINE,
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    KEY_LOAD_DELTA_MIN + ": ",
                                    className='label_class',
                                    style={
                                        'display': INLINE,
                                    }
                                ),
                                html.Label(
                                    "0",
                                    id=ID_DELTA_LOAD_MIN,
                                    className='label_class',
                                    style={
                                        'display': INLINE,
                                    }
                                ),
                            ],
                            style={
                                'margin-left': '40%',
                            }
                        ),
                        html.Div(
                            [
                                html.Label(
                                    KEY_LOAD_DELTA_MAX + ": ",
                                    className='label_class',
                                    style={
                                        'display': INLINE,
                                    }
                                ),
                                html.Label(
                                    "0",
                                    id=ID_DELTA_LOAD_MAX,
                                    className='label_class',
                                    style={
                                        'display': INLINE,
                                    }
                                ),
                            ],
                            style={
                                'margin-left': '40%',
                            }
                        ),
                    ],
                    className='row',
                    style={
                        'display': INLINE,
                        'width': '400px',
                    }
                ),
            ],
            id=ID_SERIAL_NUMBER_AREA,
            style={
                'margin-left': MARGIN,
                'margin-top': '1vw',
            }
        ),

        html.Div(
            children=[
                dash_table.DataTable(
                    id=ID_TABLE_LOAD,
                    merge_duplicate_headers=True,
                    columns=[
                        {'name': ["LOAD", "Channel"], 'id': KEY_CHANNEL},
                        {'name': ["LOAD", "Start"], 'id': KEY_LOAD_INIT},
                        {'name': ["LOAD", "Stop"], 'id': KEY_LOAD_STOP},
                        {'name': ["LOAD", "MIN"], 'id': KEY_LOAD_MIN},
                        {'name': ["LOAD", "MAX"], 'id': KEY_LOAD_MAX},
                    ],
                    data=pd.DataFrame(data=LOAD_DATA_DICTIONARY).to_dict('records'),
                    editable=False,
                    style_cell={
                        'backgroundColor': COLOR_PURPLE_LIGHT,
                        'color': COLOR_AZURE_LIGHT,
                    },
                    style_data={
                        'border': TABLE_BORDER,
                        'overflow': OVERFLOW_HIDDEN,
                        'textOverflow': OVERFLOW_ELLIPSIS,
                        'textAlign': ALIGN_CENTER,
                        'color': COLOR_GREEN_LIGHT,
                        'fontWeight': FONT_BOLD,
                        'fontSize': TABLE_DATA_SIZE,
                        'width': TABLE_CELL_FAKE_WIDTH,
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'color': COLOR_ORANGE,
                        },
                    ],
                    style_header={
                        'border': HEADER_BORDER,
                        'backgroundColor': HEADER_BACKGROUND,
                        'color': HEADER_COLOR,
                        'font': HEADER_FONT,
                        'fontSize': HEADER_FONT_SIZE,
                        'textAlign': HEADER_TEXT_ALIGN,
                        'textOverflow': HEADER_TEXT_OVERFLOW,
                    }
                ),
                html.Div(
                    id=ID_GRAPH_LOAD,
                ),
            ],
            style={
                'margin-right': MARGIN,
                'margin-left': MARGIN,
                'margin-top': MARGIN,
            }
        ),

        html.Div(
            children=[
                dash_table.DataTable(
                    id=ID_TABLE_TEMP,
                    merge_duplicate_headers=True,
                    columns=[
                        {'name': ["TEMPERATURE", "Channel"], 'id': KEY_CHANNEL},
                        {'name': ["TEMPERATURE", "Start"], 'id': KEY_TEMP_INIT},
                        {'name': ["TEMPERATURE", "Stop"], 'id': KEY_TEMP_STOP},
                        {'name': ["TEMPERATURE", "MIN"], 'id': KEY_TEMP_MIN},
                        {'name': ["TEMPERATURE", "MAX"], 'id': KEY_TEMP_MAX},
                    ],
                    data=pd.DataFrame(data=TEMP_DATA_DICTIONARY).to_dict('records'),
                    editable=False,
                    style_cell={
                        'backgroundColor': COLOR_PURPLE_LIGHT,
                        'color': COLOR_AZURE_LIGHT,
                    },
                    style_data={
                        'border': TABLE_BORDER,
                        'overflow': OVERFLOW_HIDDEN,
                        'textOverflow': OVERFLOW_ELLIPSIS,
                        'textAlign': ALIGN_CENTER,
                        'color': COLOR_GREEN_LIGHT,
                        'fontWeight': FONT_BOLD,
                        'fontSize': TABLE_DATA_SIZE,
                        'width': TABLE_CELL_FAKE_WIDTH,
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'color': COLOR_ORANGE,
                        },
                    ],
                    style_header={
                        'border': HEADER_BORDER,
                        'backgroundColor': HEADER_BACKGROUND,
                        'color': HEADER_COLOR,
                        'font': HEADER_FONT,
                        'fontSize': HEADER_FONT_SIZE,
                        'textAlign': HEADER_TEXT_ALIGN,
                        'textOverflow': HEADER_TEXT_OVERFLOW,
                    }
                ),
                html.Div(
                    id=ID_GRAPH_TEMP,
                ),
            ],
            style={
                'margin-right': MARGIN,
                'margin-left': MARGIN,
                'margin-top': MARGIN,
            }
        ),

        html.Div(
            children=[
                dash_table.DataTable(
                    id=ID_TABLE_DERI,
                    merge_duplicate_headers=True,
                    columns=[
                        {'name': ["", "Channel"], 'id': KEY_CHANNEL},
                        {'name': ["dLoad/dT", "MIN"], 'id': KEY_DLDT_MIN},
                        {'name': ["dLoad/dT", "MAX"], 'id': KEY_DLDT_MAX},
                        {'name': ["MASSIMA DIFF DA START", KEY_DIFF_MIN], 'id': KEY_DIFF_MIN},
                        {'name': ["MASSIMA DIFF DA START", KEY_DIFF_MAX], 'id': KEY_DIFF_MAX},
                    ],
                    data=pd.DataFrame(data=DERI_DATA_DICTIONARY).to_dict('records'),
                    editable=False,
                    style_cell={
                        'backgroundColor': COLOR_PURPLE_LIGHT,
                        'color': COLOR_AZURE_LIGHT,
                    },
                    style_data={
                        'border': TABLE_BORDER,
                        'overflow': OVERFLOW_HIDDEN,
                        'textOverflow': OVERFLOW_ELLIPSIS,
                        'textAlign': ALIGN_CENTER,
                        'color': COLOR_GREEN_LIGHT,
                        'fontWeight': FONT_BOLD,
                        'fontSize': TABLE_DATA_SIZE,
                        'width': TABLE_CELL_FAKE_WIDTH,
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'color': COLOR_ORANGE,
                        },
                    ],
                    style_header={
                        'border': HEADER_BORDER,
                        'backgroundColor': HEADER_BACKGROUND,
                        'color': HEADER_COLOR,
                        'font': HEADER_FONT,
                        'fontSize': HEADER_FONT_SIZE,
                        'textAlign': HEADER_TEXT_ALIGN,
                        'textOverflow': HEADER_TEXT_OVERFLOW,
                    }
                ),
                html.Div(
                    id=ID_GRAPH_DERI,
                ),
            ],
            style={
                'margin-right': MARGIN,
                'margin-left': MARGIN,
                'margin-top': MARGIN,
            }
        ),
    ]
)


# -------------------------------------------------------
# Updates the selectable SN
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_SELECT_SERIAL_NUMBER, component_property='options'),
    Input(component_id=ID_LAYOUT_SINGLE, component_property='data'),
)
def updateSN(json_data):
    if DEBUG_ACTIVE:
        print(TAG + "updateSN()")

    options = []

    if json_data is not None:
        data_frame = pd.read_json(json_data, orient='split')
        serial_numbers = data_frame[KEY_SN]
        num_perni = 0

        data_frame[KEY_SN].fillna('999999', inplace=True)

        len_test = len(serial_numbers)

        for index in range(len_test):
            if int(serial_numbers[index]) != 999999:
                options.append({"label": str(int(serial_numbers[index])), "value": str(int(serial_numbers[index]))})
                num_perni += 1

    return options


# -------------------------------------------------------
# csv file loading
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_LAYOUT_SINGLE, component_property='data'),
    Input(component_id=ID_UPDATE_FILE, component_property='contents'),
)
def updateData(dcc_upload):
    if DEBUG_ACTIVE:
        print(TAG + "updateData()")

    return updateByFile(dcc_upload)


# -------------------------------------------------------
#
# -------------------------------------------------------
def buildPlot(plot_to_build, y_title, ch1_header, ch2_header):
    plot_to_build.update_traces(
        mode='lines+markers',
        showlegend=False,
        line=dict(
            width=1.5,
            color=COLOR_GREEN_LIGHT
        ),
        marker=dict(
            size=10,
            color=COLOR_GREEN_LIGHT,
            line=dict(width=0.3, color=COLOR_GREEN_LIGHT),
            symbol='x-open'
        ),
        selector=dict(
            name=ch1_header,
            mode='markers'
        )
    )

    plot_to_build.update_traces(
        mode='lines+markers',
        showlegend=False,
        line=dict(
            width=1.5,
            color=COLOR_ORANGE
        ),
        marker=dict(
            size=10,
            color=COLOR_ORANGE,
            line=dict(width=0.3, color=COLOR_ORANGE),
            symbol='x-open'
        ),
        selector=dict(
            name=ch2_header,
            mode='markers'
        )
    )

    plot_to_build.update_xaxes(title_text="time")
    plot_to_build.update_yaxes(title_text=y_title)

    plot_to_build.update_layout(paper_bgcolor=COLOR_PURPLE_DARK)


@app.callback(
    Output(component_id=ID_GRAPH_LOAD, component_property='children'),
    Output(component_id=ID_GRAPH_TEMP, component_property='children'),
    Output(component_id=ID_GRAPH_DERI, component_property='children'),
    Input(component_id=ID_SELECT_SERIAL_NUMBER, component_property='value'),
    Input(component_id=ID_LAYOUT_SINGLE, component_property='data'),
)
def updateGraph(selected_serial_number, json_data):
    if DEBUG_ACTIVE:
        print(TAG + "updateGraph()")

    if selected_serial_number is None or json_data is None:
        return None, None, None

    ID_NODE_CH1 = 23
    ID_NODE_CH2 = 24

    ch1_load_header = None
    ch2_load_header = None
    ch1_temp_header = None
    ch2_temp_header = None
    ch1_dldt_header = None
    ch2_dldt_header = None

    ch1_load_axis_y = None
    ch2_load_axis_y = None
    ch1_temp_axis_y = None
    ch2_temp_axis_y = None
    ch1_dldt_axis_y = None
    ch2_dldt_axis_y = None

    serial_number_index = 0
    stop_while = False
    axis_x = None

    data_frame = pd.read_json(json_data, orient='split')
    data_frame[KEY_SN].fillna('999999', inplace=True)

    serial_numbers = data_frame[KEY_SN]

    while serial_number_index < len(serial_numbers) and not stop_while:
        value = int(serial_numbers[serial_number_index])

        if selected_serial_number == str(value):
            stop_while = True

            axis_x = KEY_READ_PREFIX + hex(ID_NODE_CH1)

            ch1_load_header = KEY_LOAD_PREFIX + hex(ID_NODE_CH1)
            ch2_load_header = KEY_LOAD_PREFIX + hex(ID_NODE_CH2)
            ch1_temp_header = KEY_TEMP_PREFIX + hex(ID_NODE_CH1)
            ch2_temp_header = KEY_TEMP_PREFIX + hex(ID_NODE_CH2)
            ch1_dldt_header = KEY_DLDT_PREFIX + hex(ID_NODE_CH1)
            ch2_dldt_header = KEY_DLDT_PREFIX + hex(ID_NODE_CH2)

            ch1_load_axis_y = data_frame[ch1_load_header]
            ch2_load_axis_y = data_frame[ch2_load_header]
            ch1_temp_axis_y = data_frame[ch1_temp_header]
            ch2_temp_axis_y = data_frame[ch2_temp_header]
            ch1_dldt_axis_y = data_frame[ch1_dldt_header]
            ch2_dldt_axis_y = data_frame[ch2_dldt_header]

        elif value == 999999:
            stop_while = True

        else:
            ID_NODE_CH1 += 2
            ID_NODE_CH2 += 2

            serial_number_index += 1

    plot_load = px.scatter(
        data_frame=data_frame,
        x=axis_x,
        y=[ch1_load_axis_y, ch2_load_axis_y],
        template=COLOR_plotly_dark,
    )
    plot_temp = px.scatter(
        data_frame=data_frame,
        x=axis_x,
        y=[ch1_temp_axis_y, ch2_temp_axis_y],
        template=COLOR_plotly_dark,
    )
    plot_deri = px.scatter(
        data_frame=data_frame,
        x=axis_x,
        y=[ch1_dldt_axis_y, ch2_dldt_axis_y],
        template=COLOR_plotly_dark,
    )

    if plot_load is not None:
        buildPlot(plot_load, "Load", ch1_load_header, ch2_load_header)

    if plot_temp is not None:
        buildPlot(plot_temp, "T", ch1_temp_header, ch2_temp_header)

    if plot_deri is not None:
        buildPlot(plot_deri, "dLoad/dT", ch1_dldt_header, ch2_dldt_header)

    plot_graph_load = dcc.Graph(
        id=ID_PLOT_LOAD,
        figure=plot_load
    )
    plot_graph_temp = dcc.Graph(
        id=ID_PLOT_TEMP,
        figure=plot_temp
    )
    plot_graph_deri = dcc.Graph(
        id=ID_PLOT_DERI,
        figure=plot_deri
    ),

    return plot_graph_load, plot_graph_temp, plot_graph_deri


# -------------------------------------------------------
# Change table cells values
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_TABLE_LOAD, component_property='data'),
    Output(component_id=ID_TABLE_TEMP, component_property='data'),
    Output(component_id=ID_TABLE_DERI, component_property='data'),
    Output(component_id=ID_DELTA_LOAD_MIN, component_property='children'),
    Output(component_id=ID_DELTA_LOAD_MAX, component_property='children'),
    Input(component_id=ID_LAYOUT_SINGLE, component_property='data'),
    Input(component_id=ID_SELECT_SERIAL_NUMBER, component_property='value'),
)
def updateCells(json_data, selected_serial_number):
    if DEBUG_ACTIVE:
        print(TAG + "updateCells()")

    if json_data is None:
        return [], [], [], "0", "0"

    data_frame = pd.read_json(json_data, orient='split')

    data_frame[KEY_SN].fillna('999999', inplace=True)

    serial_numbers = data_frame[KEY_SN]
    serial_number_index = 0
    ch1_num_elements = 0
    ch2_num_elements = 0
    ch1_id = 23
    ch2_id = 24
    ch1_load = 0
    ch2_load = 0
    ch1_load_init = 0
    ch2_load_init = 0
    ch1_load_stop = 0
    ch2_load_stop = 0
    ch1_load_min = 0
    ch2_load_min = 0
    ch1_load_max = 0
    ch2_load_max = 0
    ch1_dldt_min = 0
    ch2_dldt_min = 0
    ch1_dldt_max = 0
    ch2_dldt_max = 0
    ch1_temp_min = 0
    ch2_temp_min = 0
    ch1_temp_max = 0
    ch2_temp_max = 0
    ch1_temp_init = 0
    ch2_temp_init = 0
    ch1_temp_stop = 0
    ch2_temp_stop = 0
    load_delta_min = 0
    load_delta_max = 0
    stop_while = False
    update_table = False

    while serial_number_index < len(serial_numbers) and not stop_while:

        if int(serial_numbers[serial_number_index]) != 999999:

            if selected_serial_number == str(int(serial_numbers[serial_number_index])):
                id_ch1_hex = hex(ch1_id)
                id_ch2_hex = hex(ch2_id)

                ch1_load_text = KEY_LOAD_PREFIX + id_ch1_hex
                ch1_dldt_text = KEY_DLDT_PREFIX + id_ch1_hex
                ch1_temp_text = KEY_TEMP_PREFIX + id_ch1_hex

                ch1_num_elements = len(data_frame[ch1_load_text])
                ch1_load = data_frame[ch1_load_text]

                ch1_load_min = data_frame[ch1_load_text].min()
                ch1_load_max = data_frame[ch1_load_text].max()
                ch1_load_init = data_frame[ch1_load_text][0]
                ch1_load_stop = data_frame[ch1_load_text][ch1_num_elements - 1]

                ch1_dldt_min = data_frame[ch1_dldt_text].min()
                ch1_dldt_max = data_frame[ch1_dldt_text].max()

                ch1_temp_init = data_frame[ch1_temp_text][0]
                ch1_temp_stop = data_frame[ch1_temp_text][ch1_num_elements - 1]
                ch1_temp_min = data_frame[ch1_temp_text].min()
                ch1_temp_max = data_frame[ch1_temp_text].max()

                ch2_load_text = KEY_LOAD_PREFIX + id_ch2_hex
                ch2_dldt_text = KEY_DLDT_PREFIX + id_ch2_hex
                ch2_temp_text = KEY_TEMP_PREFIX + id_ch2_hex

                ch2_num_elements = len(data_frame[ch2_load_text])
                ch2_load = data_frame[ch2_load_text]

                ch2_load_init = data_frame[ch2_load_text][0]
                ch2_load_stop = data_frame[ch2_load_text][ch2_num_elements - 1]
                ch2_load_min = data_frame[ch2_load_text].min()
                ch2_load_max = data_frame[ch2_load_text].max()

                ch2_temp_init = data_frame[ch2_temp_text][0]
                ch2_temp_stop = data_frame[ch2_temp_text][ch2_num_elements - 1]
                ch2_temp_min = data_frame[ch2_temp_text].min()
                ch2_temp_max = data_frame[ch2_temp_text].max()

                ch2_dldt_min = data_frame[ch2_dldt_text].min()
                ch2_dldt_max = data_frame[ch2_dldt_text].max()

                stop_while = True
                update_table = True
            else:
                serial_number_index += 1
                ch1_id += 2
                ch2_id += 2
                pass
        else:
            serial_number_index += 1

    load_data_dictionary = {
        KEY_CHANNEL: [],
        KEY_LOAD_INIT: [],
        KEY_LOAD_STOP: [],
        KEY_LOAD_MIN: [],
        KEY_LOAD_MAX: [],
    }
    temp_data_dictionary = {
        KEY_CHANNEL: [],
        KEY_TEMP_MIN: [],
        KEY_TEMP_MAX: [],
        KEY_TEMP_INIT: [],
        KEY_TEMP_STOP: [],
    }
    deri_data_dictionary = {
        KEY_CHANNEL: [],
        KEY_DLDT_MIN: [],
        KEY_DLDT_MAX: [],
        KEY_DIFF_MIN: [],
        KEY_DIFF_MAX: [],
    }

    if update_table:
        ch1_diff_min, ch1_diff_max, ch2_diff_min, ch2_diff_max, load_delta_min, load_delta_max = updateCellsAux(
            ch1_num_elements, ch2_num_elements, ch1_load, ch2_load)

        id_ch1_hex = hex(ch1_id)
        id_ch2_hex = hex(ch2_id)

        load_data_dictionary = {
            KEY_CHANNEL: [id_ch1_hex, id_ch2_hex],
            KEY_LOAD_INIT: [ch1_load_init, ch2_load_init],
            KEY_LOAD_STOP: [ch1_load_stop, ch2_load_stop],
            KEY_LOAD_MIN: [ch1_load_min, ch2_load_min],
            KEY_LOAD_MAX: [ch1_load_max, ch2_load_max],
        }
        temp_data_dictionary = {
            KEY_CHANNEL: [id_ch1_hex, id_ch2_hex],
            KEY_TEMP_MIN: [ch1_temp_min, ch2_temp_min],
            KEY_TEMP_MAX: [ch1_temp_max, ch2_temp_max],
            KEY_TEMP_INIT: [ch1_temp_init, ch2_temp_init],
            KEY_TEMP_STOP: [ch1_temp_stop, ch2_temp_stop],
        }
        deri_data_dictionary = {
            KEY_CHANNEL: [id_ch1_hex, id_ch2_hex],
            KEY_DLDT_MIN: [ch1_dldt_min, ch2_dldt_min],
            KEY_DLDT_MAX: [ch1_dldt_max, ch2_dldt_max],
            KEY_DIFF_MIN: [ch1_diff_min, ch2_diff_min],
            KEY_DIFF_MAX: [ch1_diff_max, ch2_diff_max],
        }

    load_data_frame = pd.DataFrame(data=load_data_dictionary)
    temp_data_frame = pd.DataFrame(data=temp_data_dictionary)
    deri_data_frame = pd.DataFrame(data=deri_data_dictionary)

    load_table_data = load_data_frame.to_dict('records')
    temp_table_data = temp_data_frame.to_dict('records')
    deri_table_data = deri_data_frame.to_dict('records')

    return load_table_data, temp_table_data, deri_table_data, str(load_delta_min), str(load_delta_max)
