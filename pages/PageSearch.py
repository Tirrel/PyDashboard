import base64
import os
import tkinter
from tkinter import filedialog

import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from App import app
from manage.FileIniHandler import FileIniHandler
from manage.TestVerifier import TestVerifier
from util.Globals import *
from util.Identifiers import *
from util.Keys import *

TAG = "PageSearch."

file_ini_handler = FileIniHandler()
search_image = base64.b64encode(open('/home/marcotirelli/PyDashboard/img/search.png', 'rb').read())

search_value = ""

if DEBUG_ACTIVE:
    search_value = "22132001"

layout = html.Div(
    style={
        'backgroundColor': COLOR_PURPLE_DARK
    },
    children=[
        dcc.Store(id=ID_LAYOUT_SEARCH),

        html.Div(
            [
                dcc.Input(
                    id=ID_SEARCH_SERIAL_NUMBER,
                    value=search_value,
                    type='seach',
                    placeholder="Insert serial number",
                    style={
                        'cursor': CURSOR_HAND,
                        'width': '300px',
                        'height': '50px',
                        'borderWidth': BORDER_WIDTH,
                        'borderStyle': BORDER_STYLE,
                        'borderRadius': BORDER_RADIUS,
                        'textAlign': ALIGN_CENTER,
                        'fontSize': TEXT_MEDIUM_SIZE,
                        'color': COLOR_GREY_LIGHT,
                        'backgroundColor': COLOR_PURPLE,
                    },
                ),

                html.Div(
                    [
                        html.Button(
                            id=ID_BUTTON_SEARCH,
                            children=[
                                html.Img(
                                    src='data:image/png;base64,{}'.format(search_image.decode()),
                                )
                            ],
                            style={
                                'padding': 0,
                                'border': 'none',
                            }
                        ),
                    ],
                    style={
                        'display': INLINE,
                        'vertical-align': ALIGN_BOTTOM,
                        'margin-left': 10,
                    }
                ),

                html.Label(
                    "Inserisci un serial number e avvia la ricerca",
                    id=ID_LABEL_CSV_DIR,
                    className='label_class',
                    style={
                        'display': INLINE,
                        'width': '50%',
                        'height': '50px',
                        'fontSize': TEXT_LARGE_SIZE,
                        'color': COLOR_GREY_LIGHT,
                        'margin-left': 150,
                    }
                ),
            ],
            style={
                'margin-left': MARGIN,
                'margin-top': '1vw',
            }
        ),

        html.Div(
            [
                html.Div(
                    [
                        dash_table.DataTable(
                            id=ID_TABLE_SEARCH,
                            columns=[
                                {'name': "File", 'id': KEY_FILE},
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
                                    'if': {'column_id': KEY_FILE},
                                    'textAlign': ALIGN_LEFT,
                                    'color': COLOR_WHITE_PURE,
                                    'cursor': CURSOR_HAND,
                                    'fontWeight': FONT_CALIBRI,
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
                                    'if': {'filter_query': '{' + KEY_ESITO + '} eq KO', 'column_id': KEY_ESITO},
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
#
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_TABLE_SEARCH, component_property='data'),
    Output(component_id=ID_LABEL_CSV_DIR, component_property='children'),
    Input(component_id=ID_BUTTON_SEARCH, component_property='n_clicks'),
    State(component_id=ID_SEARCH_SERIAL_NUMBER, component_property='value'),
)
def clickSearch(n_clicks, serial_number_to_find):
    if DEBUG_ACTIVE:
        print(TAG + "clickSearch()")

    if n_clicks is None or serial_number_to_find is None or serial_number_to_find == "":
        raise PreventUpdate

    root = tkinter.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory()
    root.destroy()

    if not os.path.isdir(dir_path):
        raise PreventUpdate

    file_paths_to_return = []

    complete_dictionary = None

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)

        if os.path.isfile(file_path) and file_path.endswith('.csv'):
            with open(file_path) as file:
                text = str(file.readlines())

                if text.__contains__(serial_number_to_find):
                    file_paths_to_return.append(file_path)

                    data_frame = pd.read_csv(file_path, sep=';')

                    if data_frame is not None:
                        data_frame = data_frame.copy()

                        json_data = data_frame.to_json(date_format='iso', orient='split')

                        verifier = TestVerifier(json_data, serial_number_to_find)
                        new_dictionary = verifier.buildDictionary()
                        new_dictionary.pop(KEY_SN, None)

                        size = new_dictionary[KEY_CHANNEL].__len__()

                        last_column = [os.path.basename(file_path)] * size
                        new_dictionary[KEY_FILE] = last_column

                        if complete_dictionary is None:
                            complete_dictionary = new_dictionary.copy()
                        else:
                            for key in complete_dictionary.keys():
                                values = complete_dictionary[key]
                                values_to_add = new_dictionary[key]

                                values.extend(values_to_add)

    data_frame = pd.DataFrame(data=complete_dictionary)
    table_data = data_frame.to_dict('records')

    return table_data, dir_path


# -------------------------------------------------------
#
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_SEARCH_SERIAL_NUMBER, component_property='value'),
    Input(component_id=ID_TABLE_SEARCH, component_property='active_cell'),
    State(component_id=ID_TABLE_SEARCH, component_property='data'),
    State(component_id=ID_LABEL_CSV_DIR, component_property='children'),
)
def clickOnCell(active_cell, data_table, csv_dir_path):
    if DEBUG_ACTIVE:
        print(TAG + "clickOnCell()")

    if active_cell is not None:
        col_id = active_cell['column_id']

        if col_id == KEY_FILE:
            row_index = active_cell['row'] if active_cell else None
            row = data_table[row_index]

            filename = row[KEY_FILE]
            filepath = csv_dir_path + "\\" + filename

            os.startfile(filepath)

    raise PreventUpdate
