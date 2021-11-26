import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from App import app
from manage.FileIniHandler import FileIniHandler
from manage.TableManager import updateByFile
from manage.TestVerifier import TestVerifier
from pages import PageSingle
from util.Globals import *
from util.Identifiers import *
from util.Keys import *

TAG = "PageTest."

file_ini_handler = FileIniHandler()


# -------------------------------------------------------
#
# -------------------------------------------------------
def buildDescriptionsDictionary():
    file_ini_handler = FileIniHandler()

    data = {
        KEY_TEST: [
            "1", "2", "3", "4", "5", "6", "7"
        ],
        KEY_DESC: [
            file_ini_handler.test_1_desc,
            file_ini_handler.test_2_desc,
            file_ini_handler.test_3_desc,
            file_ini_handler.test_4_desc,
            file_ini_handler.test_5_desc,
            file_ini_handler.test_6_desc,
            file_ini_handler.test_7_desc,
        ],
        KEY_TH_MIN: [
            file_ini_handler.test_1_th_min,
            file_ini_handler.test_2_th_min,
            file_ini_handler.test_3_th_min,
            file_ini_handler.test_4_th_min,
            file_ini_handler.test_5_th_min,
            file_ini_handler.test_6_th_min,
            file_ini_handler.test_7_th_min,
        ],
        KEY_TH_MAX: [
            file_ini_handler.test_1_th_max,
            file_ini_handler.test_2_th_max,
            file_ini_handler.test_3_th_max,
            file_ini_handler.test_4_th_max,
            file_ini_handler.test_5_th_max,
            file_ini_handler.test_6_th_max,
            file_ini_handler.test_7_th_max,
        ],
    }

    return data


layout = html.Div(
    style={
        'backgroundColor': COLOR_PURPLE_DARK
    },
    children=[
        dcc.Store(id=ID_LAYOUT_TEST),

        html.Div(
            [
                html.Div(
                    [
                        dash_table.DataTable(
                            id=ID_TABLE_DESC,
                            columns=[
                                {'name': "Test", 'id': KEY_TEST},
                                {'name': "Description", 'id': KEY_DESC},
                                {'name': "Threshold MIN", 'id': KEY_TH_MIN},
                                {'name': "Threshold MAX", 'id': KEY_TH_MAX},
                            ],
                            data=pd.DataFrame(data=buildDescriptionsDictionary()).to_dict('records'),
                            editable=False,
                            page_size=7,
                            style_cell={
                                'backgroundColor': COLOR_PURPLE_LIGHT,
                                'color': COLOR_AZURE_LIGHT,
                                'width': 50,
                            },
                            style_data={
                                'border': TABLE_BORDER,
                                'overflow': OVERFLOW_HIDDEN,
                                'textOverflow': OVERFLOW_ELLIPSIS,
                                'fontSize': TEXT_SMALL_SIZE,
                                'textAlign': ALIGN_CENTER,
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': COLOR_PURPLE
                                },
                                {
                                    'if': {'column_id': KEY_TEST},
                                    'width': '80px'
                                },
                                {
                                    'if': {'column_id': KEY_DESC},
                                    'width': COLUMN_WIDTH_DESC,
                                    'textAlign': ALIGN_LEFT,
                                },
                                {
                                    'if': {'column_id': KEY_TH_MIN},
                                    'width': COLUMN_WIDTH_THRESHOLD,
                                },
                                {
                                    'if': {'column_id': KEY_TH_MAX},
                                    'width': COLUMN_WIDTH_THRESHOLD,
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
                    ]
                ),

                html.Br(),

                html.Div(
                    [
                        dash_table.DataTable(
                            id=ID_TABLE_TEST,
                            columns=[
                                {'name': "SN", 'id': KEY_SN},
                                {'name': "Channel", 'id': KEY_CHANNEL},
                                {'name': "Test 1", 'id': KEY_TEST_1},
                                {'name': "Test 2", 'id': KEY_TEST_2},
                                {'name': "Test 3", 'id': KEY_TEST_3},
                                {'name': "Test 4", 'id': KEY_TEST_4},
                                {'name': "Test 5", 'id': KEY_TEST_5},
                                {'name': "Test 6", 'id': KEY_TEST_6},
                                {'name': "Test 7", 'id': KEY_TEST_7},
                                {'name': "Test 8", 'id': KEY_TEST_8},
                                {'name': "Esito", 'id': KEY_ESITO},
                            ],
                            editable=False,
                            page_size=NUMERO_RIGHE,
                            style_cell={
                                'backgroundColor': COLOR_PURPLE_LIGHT,
                                'color': COLOR_AZURE_LIGHT,
                            },
                            style_data={
                                'border': TABLE_BORDER,
                                'overflow': OVERFLOW_HIDDEN,
                                'textOverflow': OVERFLOW_ELLIPSIS,
                                'textAlign': ALIGN_CENTER,
                                'fontSize': TABLE_DATA_SIZE,
                                'fontWeight': FONT_BOLD,
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': COLOR_PURPLE,
                                },
                                {
                                    'if': {'row_index': 'odd', 'column_id': KEY_CHANNEL},
                                    'color': COLOR_ORANGE,
                                },
                                {
                                    'if': {'row_index': 'even', 'column_id': KEY_CHANNEL},
                                    'color': COLOR_GREEN_LIGHT,
                                },
                                {
                                    'if': {'column_id': KEY_SN},
                                    'color': COLOR_WHITE_PURE,
                                    'cursor': CURSOR_HAND,
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_1 + '} eq OK', 'column_id': KEY_TEST_1},
                                    'backgroundColor': COLOR_GREEN_PURE,
                                    'color': COLOR_WHITE_PURE
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_2 + '} eq OK', 'column_id': KEY_TEST_2},
                                    'backgroundColor': COLOR_GREEN_PURE,
                                    'color': COLOR_WHITE_PURE
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_3 + '} eq OK', 'column_id': KEY_TEST_3},
                                    'backgroundColor': COLOR_GREEN_PURE,
                                    'color': COLOR_WHITE_PURE
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_4 + '} eq OK', 'column_id': KEY_TEST_4},
                                    'backgroundColor': COLOR_GREEN_PURE,
                                    'color': COLOR_WHITE_PURE
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_5 + '} eq OK', 'column_id': KEY_TEST_5},
                                    'backgroundColor': COLOR_GREEN_PURE,
                                    'color': COLOR_WHITE_PURE
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_6 + '} eq OK', 'column_id': KEY_TEST_6},
                                    'backgroundColor': COLOR_GREEN_PURE,
                                    'color': COLOR_WHITE_PURE
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_7 + '} eq OK', 'column_id': KEY_TEST_7},
                                    'backgroundColor': COLOR_GREEN_PURE,
                                    'color': COLOR_WHITE_PURE
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_8 + '} eq OK', 'column_id': KEY_TEST_8},
                                    'backgroundColor': COLOR_GREEN_PURE,
                                    'color': COLOR_WHITE_PURE
                                },
                                {
                                    'if': {'filter_query': '{ESITO} eq OK', 'column_id': KEY_ESITO, },
                                    'backgroundColor': COLOR_GREEN_PURE,
                                    'color': COLOR_WHITE_PURE
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_1 + '} eq KO', 'column_id': KEY_TEST_1},
                                    'backgroundColor': COLOR_RED_LIGHT,
                                    'color': COLOR_WHITE_PURE,
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_2 + '} eq KO', 'column_id': KEY_TEST_2},
                                    'backgroundColor': COLOR_RED_LIGHT,
                                    'color': COLOR_WHITE_PURE,
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_3 + '} eq KO', 'column_id': KEY_TEST_3},
                                    'backgroundColor': COLOR_RED_LIGHT,
                                    'color': COLOR_WHITE_PURE,
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_4 + '} eq KO', 'column_id': KEY_TEST_4},
                                    'backgroundColor': COLOR_RED_LIGHT,
                                    'color': COLOR_WHITE_PURE,
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_5 + '} eq KO', 'column_id': KEY_TEST_5},
                                    'backgroundColor': COLOR_RED_LIGHT,
                                    'color': COLOR_WHITE_PURE,
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_6 + '} eq KO', 'column_id': KEY_TEST_6},
                                    'backgroundColor': COLOR_RED_LIGHT,
                                    'color': COLOR_WHITE_PURE,
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_7 + '} eq KO', 'column_id': KEY_TEST_7},
                                    'backgroundColor': COLOR_RED_LIGHT,
                                    'color': COLOR_WHITE_PURE,
                                },
                                {
                                    'if': {'filter_query': '{' + KEY_TEST_8 + '} eq KO', 'column_id': KEY_TEST_8},
                                    'backgroundColor': COLOR_RED_LIGHT,
                                    'color': COLOR_WHITE_PURE,
                                },
                                {
                                    'if': {'filter_query': '{ESITO} eq KO', 'column_id': KEY_ESITO},
                                    'backgroundColor': COLOR_RED_LIGHT,
                                    'color': COLOR_WHITE_PURE,
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

        html.Br(),
    ]
)


# -------------------------------------------------------
# csv file loading
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_LAYOUT_TEST, component_property='data'),
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
    Output(component_id=ID_TABLE_TEST, component_property='data'),
    Input(component_id=ID_LAYOUT_TEST, component_property='data'),
)
def updateCells(json_data):
    if DEBUG_ACTIVE:
        print(TAG + "updateCells()")

    if json_data is None:
        return []

    verifier = TestVerifier(json_data, None)
    data_dictionary = verifier.buildDictionary()

    data_frame = pd.DataFrame(data=data_dictionary)
    table_data = data_frame.to_dict('records')

    return table_data


# -------------------------------------------------------
#
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_URL, component_property='pathname'),
    Input(component_id=ID_TABLE_TEST, component_property='active_cell'),
    State(component_id=ID_TABLE_TEST, component_property='data')
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

            dropdown = PageSingle.layout[ID_SELECT_SERIAL_NUMBER]
            dropdown.value = serial_number

            return HREF_PAGE_SINGLE

    raise PreventUpdate
