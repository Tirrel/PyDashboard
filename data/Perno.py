from util.Keys import *


class Perno(object):

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def __init__(self, sn):
        self.serial_number = sn
        self.ch1 = None
        self.ch2 = None
        self.ch1_esito = None
        self.ch2_esito = None
        self.skip = False
        self.ch1_colummn_read = None
        self.ch1_column_load = None
        self.ch1_column_dldt = None
        self.ch1_colummn_temp = None
        self.ch2_colummn_read = None
        self.ch2_column_load = None
        self.ch2_column_dldt = None
        self.ch2_colummn_temp = None

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def getTitleColumnLoadCh1(self):
        return KEY_LOAD_PREFIX + self.ch1

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def getTitleColumnLoadCh2(self):
        return KEY_LOAD_PREFIX + self.ch2

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def getTitleColumnDLDTCh1(self):
        return KEY_DLDT_PREFIX + self.ch1

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def getTitleColumnDLDTCh2(self):
        return KEY_DLDT_PREFIX + self.ch2
