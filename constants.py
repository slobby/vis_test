# -*- coding: utf-8 -*-
"""Application constants
"""

# Config description dir path
CONFIG = "config"

# Default description file path
DEF_DESC_PATH = "config/default_description.csv"

# Source description dir
SOURCE_DESC_DIR = "stations"

# Source description file
SOURCE_DESC_SUFIX = "description.csv"

# Source output dir
OUTPUT_DIR = "output"

# Source output postfix
OUTPUT_FILE_POSTFIX = "_out"

# Source output log postfix
OUTPUT_FILE_LOG_POSTFIX = "_log"

# Code page for description file
CONV_ENCODING = 'utf-8'

# Separator for description file
CONV_SEP = ';'

# Comment sign for description file
CONV_COMMENT = '#'

# Separator for colors in description file
COLORS_SEP = ','

# Code page for test files
TEST_ENCODING = 'utf-8'

# Separator for test files
TEST_FILE_SEP = ':'

# Log file path
PROTOCOL_CSV = "log/log.csv"

# Code page for bytes message
CODE_PAGE = "cp1251"

# socket timeout
TIMEOUT = 1

# Amount of reconnecting attempts
CON_ATTEMPTS = 5

# Message command perifix
CMD_PREFIX = 'CMD'

# Message get state perifix
GET_PREFIX = 'GET'

# Positive answer on sending command to visualisation
RESPONSE_OK_ANSWER = 'OK'

# Negative answer on sending command to visualisation
RESPONSE_NO_ANSWER = 'NO'

# Error answer on sending command to visualisation
RESPONSE_ERROR_ANSWER = 'ERR_FORMAT'

# Enviroment key for verbose mode (YES/NO)
VIS_TEST_VERBOSE = "VIS_TEST_VERBOSE"

# Enable verbose mode
VIS_TEST_VERBOSE_YES = "YES"
