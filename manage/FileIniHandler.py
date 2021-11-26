from configparser import ConfigParser

INI_FILE_NAME = './main.ini'

SECTION_MAIN = "MAIN"
SECTION_TEST = "TEST"

OPTION_TEST_1_DESC = "test_1_desc"
OPTION_TEST_1_TH_MIN = "test_1_th_min"
OPTION_TEST_1_TH_MAX = "test_1_th_max"
OPTION_TEST_2_DESC = "test_2_desc"
OPTION_TEST_2_TH_MIN = "test_2_th_min"
OPTION_TEST_2_TH_MAX = "test_2_th_max"
OPTION_TEST_3_DESC = "test_3_desc"
OPTION_TEST_3_TH_MIN = "test_3_th_min"
OPTION_TEST_3_TH_MAX = "test_3_th_max"
OPTION_TEST_4_DESC = "test_4_desc"
OPTION_TEST_4_TH_MIN = "test_4_th_min"
OPTION_TEST_4_TH_MAX = "test_4_th_max"
OPTION_TEST_5_DESC = "test_5_desc"
OPTION_TEST_5_TH_MIN = "test_5_th_min"
OPTION_TEST_5_TH_MAX = "test_5_th_max"
OPTION_TEST_6_DESC = "test_6_desc"
OPTION_TEST_6_TH_MIN = "test_6_th_min"
OPTION_TEST_6_TH_MAX = "test_6_th_max"
OPTION_TEST_7_DESC = "test_7_desc"
OPTION_TEST_7_TH_MIN = "test_7_th_min"
OPTION_TEST_7_TH_MAX = "test_7_th_max"

OPTION_INI_FILE_PATH = "ini_file_path"


class FileIniHandler(object):

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def __init__(self):
        self.test_1_desc = ""
        self.test_1_th_min = ""
        self.test_1_th_max = ""

        self.test_2_desc = ""
        self.test_2_th_min = ""
        self.test_2_th_max = ""

        self.test_3_desc = ""
        self.test_3_th_min = ""
        self.test_3_th_max = ""

        self.test_4_desc = ""
        self.test_4_th_min = ""
        self.test_4_th_max = ""

        self.test_5_desc = ""
        self.test_5_th_min = ""
        self.test_5_th_max = ""

        self.test_6_desc = ""
        self.test_6_th_min = ""
        self.test_6_th_max = ""

        self.test_7_desc = ""
        self.test_7_th_min = ""
        self.test_7_th_max = ""

        self.ini_file_path = ""

        self.config_parser = ConfigParser()

        self.read()

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    def read(self):
        self.config_parser.read(INI_FILE_NAME)

        if self.config_parser.has_section(SECTION_MAIN):
            if self.config_parser.has_option(SECTION_MAIN, OPTION_INI_FILE_PATH):
                self.ini_file_path = self.config_parser.get(SECTION_MAIN, OPTION_INI_FILE_PATH)

        if self.config_parser.has_section(SECTION_TEST):
            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_1_DESC):
                self.test_1_desc = self.config_parser.get(SECTION_TEST, OPTION_TEST_1_DESC)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_1_TH_MIN):
                self.test_1_th_min = self.config_parser.get(SECTION_TEST, OPTION_TEST_1_TH_MIN)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_1_TH_MAX):
                self.test_1_th_max = self.config_parser.get(SECTION_TEST, OPTION_TEST_1_TH_MAX)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_2_DESC):
                self.test_2_desc = self.config_parser.get(SECTION_TEST, OPTION_TEST_2_DESC)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_2_TH_MIN):
                self.test_2_th_min = self.config_parser.get(SECTION_TEST, OPTION_TEST_2_TH_MIN)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_2_TH_MAX):
                self.test_2_th_max = self.config_parser.get(SECTION_TEST, OPTION_TEST_2_TH_MAX)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_3_DESC):
                self.test_3_desc = self.config_parser.get(SECTION_TEST, OPTION_TEST_3_DESC)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_3_TH_MIN):
                self.test_3_th_min = self.config_parser.get(SECTION_TEST, OPTION_TEST_3_TH_MIN)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_3_TH_MAX):
                self.test_3_th_max = self.config_parser.get(SECTION_TEST, OPTION_TEST_3_TH_MAX)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_4_DESC):
                self.test_4_desc = self.config_parser.get(SECTION_TEST, OPTION_TEST_4_DESC)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_4_TH_MIN):
                self.test_4_th_min = self.config_parser.get(SECTION_TEST, OPTION_TEST_4_TH_MIN)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_4_TH_MAX):
                self.test_4_th_max = self.config_parser.get(SECTION_TEST, OPTION_TEST_4_TH_MAX)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_5_DESC):
                self.test_5_desc = self.config_parser.get(SECTION_TEST, OPTION_TEST_5_DESC)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_5_TH_MIN):
                self.test_5_th_min = self.config_parser.get(SECTION_TEST, OPTION_TEST_5_TH_MIN)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_5_TH_MAX):
                self.test_5_th_max = self.config_parser.get(SECTION_TEST, OPTION_TEST_5_TH_MAX)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_6_DESC):
                self.test_6_desc = self.config_parser.get(SECTION_TEST, OPTION_TEST_6_DESC)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_6_TH_MIN):
                self.test_6_th_min = self.config_parser.get(SECTION_TEST, OPTION_TEST_6_TH_MIN)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_6_TH_MAX):
                self.test_6_th_max = self.config_parser.get(SECTION_TEST, OPTION_TEST_6_TH_MAX)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_7_DESC):
                self.test_7_desc = self.config_parser.get(SECTION_TEST, OPTION_TEST_7_DESC)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_7_TH_MIN):
                self.test_7_th_min = self.config_parser.get(SECTION_TEST, OPTION_TEST_7_TH_MIN)

            if self.config_parser.has_option(SECTION_TEST, OPTION_TEST_7_TH_MAX):
                self.test_7_th_max = self.config_parser.get(SECTION_TEST, OPTION_TEST_7_TH_MAX)
