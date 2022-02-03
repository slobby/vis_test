import os
from exceptions import DublicateKeyException, UnhandledRowException
from row_handler.ColorRowHandler import ColorRowHandler
from row_handler.ObjectRowHandler import ObjectRowHandler
from row_handler.StateRowHandler import StateRowHandler
from row_handler.UnhandledRowHandler import UnhandledRowHandler
from constants import CONV_COMMENT, CONV_ENCODING, CONV_SEP, CONVENTIONS
from logger import get_logger

logger = get_logger(__name__)


class Station:
    objects: dict[int, set[str]]
    ungatherd_objects: dict[str, int]
    colors: dict[str, set[int]]
    states: dict[int, int]

    def __init__(self, name) -> None:
        self.conf_path = CONVENTIONS
        self.objects = dict()
        self.colors = dict()
        self.states = dict()
        self.ungatherd_objects = dict()
        self.fill_dict()

    def fill_dict(self):
        color_handler = ColorRowHandler()
        object_handler = ObjectRowHandler()
        state_handler = StateRowHandler()
        unhandled_row_handler = UnhandledRowHandler()
        object_handler.setNext(color_handler)
        color_handler.setNext(state_handler)
        state_handler.setNext(unhandled_row_handler)
        with open(self.conf_path, mode='r', encoding=CONV_ENCODING) as fs:
            for raw_line in fs:
                line, _, _ = raw_line.strip(' \n').partition(CONV_COMMENT)
                if line:
                    row = line.split(CONV_SEP)
                    try:
                        if row:
                            row = [item.strip(' \n') for item in row]
                            object_handler.handle(row, self)
                    except (ValueError, KeyError):
                        logger.error(f'Error while parsing the row [{line}]')
                    except DublicateKeyException:
                        logger.warning(
                            f'Dublicate value for key in the row [{line}]')
                    except UnhandledRowException:
                        logger.error(f'Couldn`t handle the row [{line}]')
