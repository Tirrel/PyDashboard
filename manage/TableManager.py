import base64
import io

import pandas as pd


# -------------------------------------------------------
#
# -------------------------------------------------------
def updateCellsAux(ch1_len, ch2_len, ch1_load, ch2_load):
    ch1_diff_min = 1000
    ch2_diff_min = 1000
    ch1_diff_max = 0
    ch2_diff_max = 0
    load_delta_min = 1000
    load_delta_max = 0

    size = min(ch1_len, ch2_len)

    for index in range(size):
        diff = abs(ch1_load[index] - ch2_load[index])

        load_delta_min = min(diff, load_delta_min)
        load_delta_max = max(diff, load_delta_max)

        ch1_delta_load = abs(ch1_load[index] - ch1_load[0])
        ch1_diff_min = min(ch1_delta_load, ch1_diff_min)
        ch1_diff_max = max(ch1_delta_load, ch1_diff_max)

        ch2_delta_load = abs(ch2_load[index] - ch2_load[0])
        ch2_diff_min = min(ch2_delta_load, ch2_diff_min)
        ch2_diff_max = max(ch2_delta_load, ch2_diff_max)

    return ch1_diff_min, ch1_diff_max, ch2_diff_min, ch2_diff_max, load_delta_min, load_delta_max


# -------------------------------------------------------
#
# -------------------------------------------------------
def parseReportFile(dcc_upload):
    content_type, content_string = dcc_upload.split(',')
    decoded = base64.b64decode(content_string)

    data_frame = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=';')

    return data_frame


# -------------------------------------------------------
# csv file loading
# -------------------------------------------------------
def updateByFile(dcc_upload):
    json_data = None

    if dcc_upload is not None:
        data_frame = parseReportFile(dcc_upload).copy()

        if data_frame is not None:
            json_data = data_frame.to_json(date_format='iso', orient='split')

    return json_data
