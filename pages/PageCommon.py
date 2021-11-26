import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from App import app
from manage.TableManager import updateCellsAux, updateByFile
from pages import PageSingle
from util.Dictionaries import *
from util.Globals import *
from util.Identifiers import *
from util.Keys import *

TAG = "PageCommon."

layout = html.Div(
    style={
        'backgroundColor': COLOR_PURPLE_DARK
    },
    children=[
        dcc.Store(id=ID_LAYOUT_COMMON),

        html.Div(
            [
                html.Div(
                    [
                        dash_table.DataTable(
                            id=ID_TABLE_COMMON,
                            merge_duplicate_headers=True,
                            columns=[
                                {'name': ["", "SN"], 'id': KEY_SN},
                                {'name': ["", "Channel"], 'id': KEY_CHANNEL},
                                {'name': ["LOAD", "Start"], 'id': KEY_LOAD_INIT},
                                {'name': ["LOAD", "Stop"], 'id': KEY_LOAD_STOP},
                                {'name': ["LOAD", "MIN"], 'id': KEY_LOAD_MIN},
                                {'name': ["LOAD", "MAX"], 'id': KEY_LOAD_MAX},
                                {'name': ["LOAD", "∆ MIN"], 'id': KEY_LOAD_DELTA_MIN},
                                {'name': ["LOAD", "∆ MAX"], 'id': KEY_LOAD_DELTA_MAX},
                                {'name': ["TEMPERATURE", "Start"], 'id': KEY_TEMP_INIT},
                                {'name': ["TEMPERATURE", "Stop"], 'id': KEY_TEMP_STOP},
                                {'name': ["TEMPERATURE", "MIN"], 'id': KEY_TEMP_MIN},
                                {'name': ["TEMPERATURE", "MAX"], 'id': KEY_TEMP_MAX},
                                {'name': ["dLoad/dT", "MIN"], 'id': KEY_DLDT_MIN},
                                {'name': ["dLoad/dT", "MAX"], 'id': KEY_DLDT_MAX},
                                {'name': ["MASSIMA DIFF DA START", "∆ MIN"], 'id': KEY_DIFF_MIN},
                                {'name': ["MASSIMA DIFF DA START", "∆ MAX"], 'id': KEY_DIFF_MAX},
                            ],
                            data=pd.DataFrame(data=COMMON_DATA_DICTIONARY).to_dict('records'),
                            editable=False,
                            page_size=NUMERO_RIGHE,
                            style_cell={
                                'backgroundColor': COLOR_PURPLE_LIGHT,
                            },
                            style_data={
                                'border': TABLE_BORDER,
                                'overflow': OVERFLOW_HIDDEN,
                                'textOverflow': OVERFLOW_ELLIPSIS,
                                'textAlign': ALIGN_CENTER,
                                'fontSize': TABLE_DATA_SIZE,
                                'fontWeight': FONT_BOLD,
                                'color': COLOR_GREEN_LIGHT,
                                'width': TABLE_CELL_FAKE_WIDTH,
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': COLOR_PURPLE,
                                    'color': COLOR_ORANGE,
                                },
                                {
                                    'if': {'column_id': KEY_SN},
                                    'color': COLOR_WHITE_PURE,
                                    'cursor': CURSOR_HAND,
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
                            },
                        ),
                    ]
                ),
            ],
            style={
                'margin-right': MARGIN,
                'margin-left': MARGIN,
                'margin-top': MARGIN,
            },
            className='row'
        ),
    ]
)


# -------------------------------------------------------
# csv file loading
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_LAYOUT_COMMON, component_property='data'),
    Input(component_id=ID_UPDATE_FILE, component_property='contents'),
)
def updateData(dcc_upload):
    if DEBUG_ACTIVE:
        print(TAG + "updateData()")

    return updateByFile(dcc_upload)


# -------------------------------------------------------
#
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_TABLE_COMMON, component_property='data'),
    Input(component_id=ID_LAYOUT_COMMON, component_property='data'),
)
def updateCells(json_data):
    if DEBUG_ACTIVE:
        print(TAG + "updateCells()")

    if json_data is None:
        return []

    data_frame = pd.read_json(json_data, orient='split')

    serial_numbers = data_frame[KEY_SN]

    model = []
    keys = []
    ch1_id = 23  # 17
    ch2_id = 24  # 18
    index = 0

    for serial_number in serial_numbers:
        if serial_number == 999999:
            continue

        ch1_id_hex = hex(ch1_id)
        ch2_id_hex = hex(ch2_id)

        ch1_load_text = KEY_LOAD_PREFIX + ch1_id_hex
        ch2_load_text = KEY_LOAD_PREFIX + ch2_id_hex
        ch1_dtdl_text = KEY_DLDT_PREFIX + ch1_id_hex
        ch2_dtdl_text = KEY_DLDT_PREFIX + ch2_id_hex
        ch1_temp_text = KEY_TEMP_PREFIX + ch1_id_hex
        ch2_temp_text = KEY_TEMP_PREFIX + ch2_id_hex

        ch1_load_values = data_frame.get(ch1_load_text)
        ch2_load_values = data_frame.get(ch2_load_text)

        if ch1_load_values is None or ch2_load_values is None:
            continue

        ch1_num_elements = len(ch1_load_values) - 1
        ch2_num_elements = len(ch2_load_values) - 1

        ch1_diff_min, ch1_diff_max, ch2_diff_min, ch2_diff_max, load_delta_min, load_delta_max = updateCellsAux(
            ch1_num_elements, ch2_num_elements, ch1_load_values, ch2_load_values)

        ch1_load_min = data_frame[ch1_load_text].min()
        ch1_load_max = data_frame[ch1_load_text].max()
        ch1_load_init = data_frame[ch1_load_text][0]
        ch1_load_stop = data_frame[ch1_load_text][ch1_num_elements]

        ch1_temp_init = data_frame[ch1_temp_text][0]
        ch1_temp_stop = data_frame[ch1_temp_text][ch1_num_elements]
        ch1_temp_min = data_frame[ch1_temp_text].min()
        ch1_temp_max = data_frame[ch1_temp_text].max()

        ch1_dldt_min = data_frame[ch1_dtdl_text].min()
        ch1_dldt_max = data_frame[ch1_dtdl_text].max()

        ch1_raw = {
            KEY_ID: [index],
            KEY_SN: [serial_number],
            KEY_CHANNEL: [ch1_id_hex],

            KEY_LOAD_INIT: [ch1_load_init],
            KEY_LOAD_STOP: [ch1_load_stop],
            KEY_LOAD_MIN: [ch1_load_min],
            KEY_LOAD_MAX: [ch1_load_max],
            KEY_LOAD_DELTA_MIN: [load_delta_min],
            KEY_LOAD_DELTA_MAX: [load_delta_max],

            KEY_TEMP_INIT: [ch1_temp_init],
            KEY_TEMP_STOP: [ch1_temp_stop],
            KEY_TEMP_MIN: [ch1_temp_min],
            KEY_TEMP_MAX: [ch1_temp_max],

            KEY_DLDT_MIN: [ch1_dldt_min],
            KEY_DLDT_MAX: [ch1_dldt_max],

            KEY_DIFF_MIN: [ch1_diff_min],
            KEY_DIFF_MAX: [ch1_diff_max],
        }

        model.append(ch1_raw)
        keys.append(index)
        index = index + 1

        ch2_load_init = data_frame[ch2_load_text][0]
        ch2_load_stop = data_frame[ch2_load_text][ch2_num_elements]
        ch2_load_min = data_frame[ch2_load_text].min()
        ch2_load_max = data_frame[ch2_load_text].max()

        ch2_temp_init = data_frame[ch2_temp_text][0]
        ch2_temp_stop = data_frame[ch2_temp_text][ch2_num_elements]
        ch2_temp_min = data_frame[ch2_temp_text].min()
        ch2_temp_max = data_frame[ch2_temp_text].max()

        ch2_dldt_min = data_frame[ch2_dtdl_text].min()
        ch2_dldt_max = data_frame[ch2_dtdl_text].max()

        ch2_raw = {
            KEY_ID: [index],
            KEY_SN: [serial_number],
            KEY_CHANNEL: [ch2_id_hex],

            KEY_LOAD_INIT: [ch2_load_init],
            KEY_LOAD_STOP: [ch2_load_stop],
            KEY_LOAD_MIN: [ch2_load_min],
            KEY_LOAD_MAX: [ch2_load_max],
            KEY_LOAD_DELTA_MIN: [load_delta_min],
            KEY_LOAD_DELTA_MAX: [load_delta_max],

            KEY_TEMP_INIT: [ch2_temp_init],
            KEY_TEMP_STOP: [ch2_temp_stop],
            KEY_TEMP_MIN: [ch2_temp_min],
            KEY_TEMP_MAX: [ch2_temp_max],

            KEY_DLDT_MIN: [ch2_dldt_min],
            KEY_DLDT_MAX: [ch2_dldt_max],

            KEY_DIFF_MIN: [ch2_diff_min],
            KEY_DIFF_MAX: [ch2_diff_max],
        }

        model.append(ch2_raw)
        keys.append(index)
        index = index + 1

        ch1_id += 2
        ch2_id += 2

    data_frame = pd.DataFrame(data=model)
    data_frame['id'] = data_frame[KEY_ID]
    data_frame.set_index('id', inplace=True, drop=False)

    table_data = data_frame.to_dict('records')

    return table_data


# -------------------------------------------------------
#
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_URL, component_property='pathname'),
    Input(component_id=ID_TABLE_COMMON, component_property='active_cell'),
    State(component_id=ID_TABLE_COMMON, component_property='data')
)
def clickOnCell(active_cell, data_table):
    if DEBUG_ACTIVE:
        print(TAG + "clickOnCell()")

    if active_cell is not None:
        col_index = active_cell['column']

        if col_index == 0:
            row_index = active_cell['row']

            row = data_table[row_index]
            serial_number = str(row[KEY_SN])
            serial_number = serial_number[1:-1]

            dropdown = PageSingle.layout[ID_SELECT_SERIAL_NUMBER]
            dropdown.value = serial_number

            return HREF_PAGE_SINGLE

    raise PreventUpdate
