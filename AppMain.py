import base64
import os
import shutil
import threading
import time
import webbrowser
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import *
from dash.exceptions import PreventUpdate
from future.moves import sys
from App import app
from manage.FileIniHandler import FileIniHandler, INI_FILE_NAME
from pages import PageCommon, PageSingle, PageTest, PageSearch
from util.Globals import *
from util.Identifiers import *

TAG = "AppMain."


# -------------------------------------------------------
#
# -------------------------------------------------------
def buildBanner():
    encoded_image = base64.b64encode(open('/home/marcotirelli/PyDashboard/img/logo.png', 'rb').read())

    return html.Div(
        id=ID_BANNER_LAYOUT,
        className="banner",
        children=[
            html.Div(
                id=ID_BANNER_SPACE,
                children=[
                    html.H6(
                        APP_NAME,
                        style={
                            'width': "1100px",
                            'text-align': ALIGN_LEFT,
                            'color': COLOR_GREY_LIGHT,
                            'fontSize': TEXT_SMALL_SIZE,
                            'padding': 10,
                        },
                    ),
                ],
                style={
                    'display': INLINE,
                    'vertical-align': ALIGN_TOP_LEFT,
                    'margin-top': '1vw'
                },
            ),
            html.Div(
                id=ID_BANNER_LOGO,
                children=[
                    html.Img(
                        id=ID_BANNER_IMAGE,
                        src='data:image/png;base64,{}'.format(encoded_image.decode()),
                        width=158,
                        height=31
                    ),
                ],
                style={
                    'display': INLINE,
                    'vertical-align': 'top-right',
                    'margin-left': '2vw',
                    'margin-top': '3vw'
                },
                className='row'
            )
        ],
    )


app.layout = html.Div(
    style={
        'backgroundColor': COLOR_PURPLE_DARK
    },
    children=[
        dcc.Location(
            id=ID_URL,
            refresh=False
        ),
        html.Div(
            [
                html.Div(
                    children=[
                        dcc.Upload(
                            id=ID_UPDATE_FILE,
                            accept='.csv',
                            multiple=False,
                            children=html.Div(
                                [
                                    "Drag and drop or click here to select files"
                                ]
                            ),
                            style={
                                'cursor': CURSOR_HAND,
                                'display': INLINE,
                                'width': '300px',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': BORDER_WIDTH,
                                'borderStyle': BORDER_STYLE,
                                'borderRadius': BORDER_RADIUS,
                                'textAlign': ALIGN_CENTER,
                                'fontSize': TEXT_MEDIUM_SIZE,
                                'color': COLOR_GREY_LIGHT,
                                'backgroundColor': COLOR_PURPLE,
                            },
                        ),
                    ],
                    style={
                        'display': INLINE,
                        'margin-left': MARGIN,
                        'margin-top': MARGIN,
                    }
                ),
                dcc.Link(
                    'Test results',
                    href=HREF_PAGE_TEST,
                    className='tab_link_class',
                    style={
                        'margin-left': '3vw',
                    },
                ),
                dcc.Link(
                    'Single report',
                    href=HREF_PAGE_SINGLE,
                    className='tab_link_class',
                    style={
                        'margin-left': '15px',
                    },
                ),
                dcc.Link(
                    'Common report',
                    href=HREF_PAGE_COMMON,
                    className='tab_link_class',
                    style={
                        'margin-left': '15px',
                    },
                ),
                dcc.Link(
                    'Search report',
                    href=HREF_PAGE_SEARCH,
                    className='tab_link_class',
                    style={
                        'margin-left': '15px',
                    },
                ),

                html.Div(
                    [
                        dcc.ConfirmDialogProvider(
                            id=ID_BUTTON_DOWNLOAD,
                            message='Sincronizzare il file .ini con quello presente in rete?',
                            children=[
                                html.Button('Sincronizza'),
                            ],
                        ),
                    ],
                    style={
                        'display': INLINE,
                        'margin-left': 100,
                    }
                ),
            ],
            className='row'
        ),

        html.Div(
            id=ID_PAGE_CONTAINER,
        ),

        buildBanner(),
    ]
)


# -------------------------------------------------------
#
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_PAGE_CONTAINER, component_property='children'),
    Input(component_id=ID_URL, component_property='pathname')
)
def clickOnPageToShow(pathname):
    if DEBUG_ACTIVE:
        print(TAG + "clickOnPageToShow(" + pathname + ")")

    return findPageToShow(pathname)


# -------------------------------------------------------
#
# -------------------------------------------------------
@app.callback(
    Output(component_id=ID_BUTTON_DOWNLOAD, component_property='data'),
    Input(component_id=ID_BUTTON_DOWNLOAD, component_property='submit_n_clicks'),
)
def clickDownload(submit_n_clicks):
    if DEBUG_ACTIVE:
        print(TAG + "clickDownload()")

    if not submit_n_clicks:
        raise PreventUpdate

    file_ini_handler = FileIniHandler()

    src = file_ini_handler.ini_file_path
    dst = INI_FILE_NAME

    if os.path.isfile(src):
        shutil.copyfile(src, dst, follow_symlinks=True)


# -------------------------------------------------------
#
# -------------------------------------------------------
def findPageToShow(pathname):
    if DEBUG_ACTIVE:
        print(TAG + "findPageToShow(" + pathname + ")")

    if pathname == HREF_PAGE_SINGLE:
        return PageSingle.layout

    elif pathname == HREF_PAGE_COMMON:
        return PageCommon.layout

    elif pathname == HREF_PAGE_SEARCH:
        return PageSearch.layout

    return PageTest.layout


# -------------------------------------------------------
#
# -------------------------------------------------------
def openBrowser():
    time.sleep(1)

    webbrowser.open('http://127.0.0.1:8050/', new=2)


if __name__ == '__main__':
    write_csv_file_tread = threading.Thread(
        target=openBrowser,
        daemon=True
    )

    write_csv_file_tread.start()

    # Rimozione del messaggio di default
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None

    app.run_server()
