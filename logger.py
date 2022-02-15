# -*- coding: utf-8 -*-
"""
Logger module

"""

import logging
import os
import sys
from constants import PROTOCOL_CSV, VIS_TEST_VERBOSE, VIS_TEST_VERBOSE_YES

log_format: str = "%(asctime)s - [%(levelname)s] - %(name)s - \
(%(filename)s:%(funcName)s:%(lineno)d) - %(message)s"


def get_file_handler(filename: str) -> logging.Handler:
    """
    create handler for writing into the file
    filename: path to file name
    """

    file_handler = logging.FileHandler(filename, encoding="utf8", delay=True)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    return file_handler


def get_stream_handler() -> logging.Handler:
    """
    create handler for writing into the stdout
    """
    logging_level = logging.WARNING
    stream_handler = logging.StreamHandler(sys.stdout)
    if os.environ.get(VIS_TEST_VERBOSE, 'NO') == VIS_TEST_VERBOSE_YES:
        logging_level = logging.INFO
    stream_handler.setLevel(logging_level)
    stream_handler.setFormatter(logging.Formatter(log_format))
    return stream_handler


def get_logger(name: str, filename: str = PROTOCOL_CSV) -> logging.Logger:
    """
    create logger
    name: logger name
    filename: path to file name
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler(filename))
    logger.addHandler(get_stream_handler())
    logger.propagate = False
    return logger
