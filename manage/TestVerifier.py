import pandas as pd

from data.Perno import Perno
from manage.FileIniHandler import FileIniHandler
from util.Globals import OK, KO, SKIP
from util.Keys import *


class TestVerifier(object):

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def __init__(self, json_data, sn_to_find=None):
        if json_data is None:
            return

        self.serial_number_to_find = sn_to_find
        self.file_ini_handler = FileIniHandler()

        self.data_frame = pd.read_json(json_data, orient='split')

        self.serial_numbers = self.data_frame[KEY_SN]
        self.num_perni_validi = 0

        # solo per i file out
        self.esito_ch1 = self.data_frame.get('ESITO_CH1')
        self.esito_ch2 = self.data_frame.get('ESITO_CH2')

        self.perni = []

        # serve per ricavare quanti valori non sono NA da cui si ricava poi il numero di perni
        series_as_booleans = self.serial_numbers.notna()
        channel_as_dec = 23  # 0x17

        for serial_number_index in range(self.serial_numbers.size):
            if series_as_booleans[serial_number_index]:
                serial_number = str(int(self.serial_numbers[serial_number_index]))

                ch1_as_hex = hex(channel_as_dec)
                channel_as_dec += 1
                ch2_as_hex = hex(channel_as_dec)
                channel_as_dec += 1

                perno = Perno(serial_number)
                perno.ch1 = ch1_as_hex
                perno.ch2 = ch2_as_hex
                perno.ch1_column_load = self.data_frame[perno.getTitleColumnLoadCh1()]
                perno.ch1_column_dldt = self.data_frame[perno.getTitleColumnDLDTCh1()]
                perno.ch2_column_load = self.data_frame[perno.getTitleColumnLoadCh2()]
                perno.ch2_column_dldt = self.data_frame[perno.getTitleColumnDLDTCh2()]

                if self.serial_number_to_find is not None and self.serial_number_to_find != serial_number:
                    perno.skip = True
                    continue

                self.num_perni_validi += 1

                self.perni.append(perno)

                if self.esito_ch1 is not None:
                    esito = self.esito_ch1[serial_number_index]
                    perno.ch1_esito = esito

                if self.esito_ch2 is not None:
                    esito = self.esito_ch2[serial_number_index]
                    perno.ch2_esito = esito

        self.column_sn = []
        self.column_ch = []

        self.initTest()

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def initTest(self):

        num_channels = 2 * self.num_perni_validi

        self.error_test_1 = [OK for _ in range(num_channels)]
        self.error_test_2 = [OK for _ in range(num_channels)]
        self.error_test_3 = [OK for _ in range(num_channels)]
        self.error_test_4 = [OK for _ in range(num_channels)]
        self.error_test_5 = [KO for _ in range(num_channels)]
        self.error_test_6 = [KO for _ in range(num_channels)]
        self.error_test_7 = [OK for _ in range(num_channels)]
        self.error_test_8 = [KO for _ in range(num_channels)]
        self.esito_dei_test = [KO for _ in range(num_channels)]

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def buildDictionary(self):

        row_index = 0

        for perno in self.perni:
            if perno.skip:
                row_index += 2
                continue

            serial_number = perno.serial_number
            channel_1 = perno.ch1
            channel_2 = perno.ch2

            self.column_sn.append(serial_number)
            self.column_sn.append(serial_number)
            self.column_ch.append(channel_1)
            self.column_ch.append(channel_2)

            ch1_column_load = perno.ch1_column_load
            ch1_column_dldt = perno.ch1_column_dldt
            ch1_esito = perno.ch1_esito

            self.startTestChannel(row_index, ch1_column_load, ch1_column_dldt, ch1_esito)

            row_index += 1

            ch2_column_load = perno.ch2_column_load
            ch2_column_dldt = perno.ch2_column_dldt
            ch2_esito = perno.ch2_esito

            self.startTestChannel(row_index, ch2_column_load, ch2_column_dldt, ch2_esito)

            len1 = len(ch1_column_load)
            len2 = len(ch2_column_load)

            if len1 <= len2:
                min_len = len1
            else:
                min_len = len2

            for sub_index in range(min_len):
                self.test3(row_index, ch2_column_load, ch1_column_load, sub_index)
                self.test5(row_index, ch2_column_load, ch1_column_load, sub_index)

            row_index += 1

        self.controllaEsito()

        data_dictionary = {
            KEY_SN: self.column_sn,
            KEY_CHANNEL: self.column_ch,
            KEY_TEST_1: self.error_test_1,
            KEY_TEST_2: self.error_test_2,
            KEY_TEST_3: self.error_test_3,
            KEY_TEST_4: self.error_test_4,
            KEY_TEST_5: self.error_test_5,
            KEY_TEST_6: self.error_test_6,
            KEY_TEST_7: self.error_test_7,
            KEY_TEST_8: self.error_test_8,
            KEY_ESITO: self.esito_dei_test
        }

        return data_dictionary

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def controllaEsito(self):
        row_index = 0

        for perno in self.perni:
            if perno.skip:
                continue

            if self.areTestOK(row_index):
                self.esito_dei_test[row_index] = OK

            row_index += 1

            if self.areTestOK(row_index):
                self.esito_dei_test[row_index] = OK

            row_index += 1

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def startTestChannel(self, row_index, column_load, column_dldt, esito):

        self.test1(row_index, column_load)

        for sub_index in range(len(column_load)):
            self.test2(row_index, column_load, sub_index)
            self.test4(row_index, column_dldt, sub_index)
            self.test6(row_index, column_load, sub_index)

        self.test7(row_index, column_load)
        self.test8(row_index, esito)

    # -------------------------------------------------------
    # TEST_1: valore iniziale singolo canale entro un certo intervallo MAX
    # -------------------------------------------------------
    def test1(self, row_index, column_load):
        first_load = column_load[0]

        th_max = int(self.file_ini_handler.test_1_th_max)
        value = abs(first_load)

        if value > th_max:
            self.error_test_1[row_index] = KO

    # -------------------------------------------------------
    # TEST_2: singolo canale entro un certo intervallo MIN-MAX rispetto al valore iniziale
    # -------------------------------------------------------
    def test2(self, row_index, column_load, sub_index):
        first_load = column_load[0]

        th_max = int(self.file_ini_handler.test_2_th_max)
        value = abs(column_load[sub_index]) - abs(first_load)

        if value > th_max:
            self.error_test_2[row_index] = KO

    # -------------------------------------------------------
    # TEST_3: valore assoluto differenza canale 1-2 sempre entro una soglia MAX
    # -------------------------------------------------------
    def test3(self, row_index, column_load, column_load_prev, sub_index):
        th_max = int(self.file_ini_handler.test_3_th_max)
        value = abs(column_load_prev[sub_index] - column_load[sub_index])

        if value > th_max:
            self.error_test_3[row_index - 1] = KO
            self.error_test_3[row_index] = KO

    # -------------------------------------------------------
    # TEST_4: valore assoluto della derivata del singolo canale sempre entro un intervallo MIN-MAX
    # -------------------------------------------------------
    def test4(self, row_index, column_dldt, sub_index):
        th_max = int(self.file_ini_handler.test_4_th_max)
        value = abs(column_dldt[sub_index])

        if value > th_max:
            self.error_test_4[row_index] = KO

    # -------------------------------------------------------
    # TEST_5: massimo del valore assoluto della differenza fra i 2 canali che NON deve stare all’interno di un intervallo MIN-MAX (tipicamente 0 e 2)
    # -------------------------------------------------------
    def test5(self, row_index, column_load, column_load_prev, sub_index):
        th_max = int(self.file_ini_handler.test_5_th_max)
        value = abs(column_load_prev[sub_index] - column_load[sub_index])

        if value > th_max:
            self.error_test_5[row_index - 1] = OK
            self.error_test_5[row_index] = OK

    # -------------------------------------------------------
    # TEST_6: massimo della differenza fra valore attuale e valore iniziale he DEVE essere maggiore di un valore minimo (tipicamente 0)
    # -------------------------------------------------------
    def test6(self, row_index, column_load, sub_index):
        first_load = column_load[0]

        th_min = int(self.file_ini_handler.test_6_th_min)
        value = abs(column_load[sub_index] - first_load)

        if value > th_min:
            self.error_test_6[row_index] = OK

    # -------------------------------------------------------
    # TEST_7: massimo della differenza fra valore finale e valore iniziale che DEVE essere minore di una soglia MAX
    # -------------------------------------------------------
    def test7(self, row_index, column_load):
        first_load = column_load[0]

        th_max = int(self.file_ini_handler.test_7_th_max)
        value = abs(column_load[len(column_load) - 1] - first_load)

        if value > th_max:
            self.error_test_7[row_index] = KO

    # -------------------------------------------------------
    # TEST_8: compensazione termica
    # -------------------------------------------------------
    def test8(self, row_index, esito):
        size = len(self.perni) * 2

        if row_index >= size:
            self.error_test_8[row_index] = SKIP
        else:
            if esito is None:
                self.error_test_8[row_index] = SKIP
            elif esito:
                self.error_test_8[row_index] = OK
            else:
                self.error_test_8[row_index] = KO

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def areTestOK(self, row_index):
        return self.error_test_1[row_index] == OK and \
               self.error_test_2[row_index] == OK and \
               self.error_test_3[row_index] == OK and \
               self.error_test_4[row_index] == OK and \
               self.error_test_5[row_index] == OK and \
               self.error_test_6[row_index] == OK and \
               self.error_test_7[row_index] == OK and \
               (self.error_test_8[row_index] == OK or self.error_test_8[row_index] == SKIP)
