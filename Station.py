import os
from ColorRowHandler import ColorRowHandler
from ObjectRowHandler import ObjectRowHandler
from StateRowHandler import StateRowHandler
from config.config import CONV_COMMENT, CONV_ENCODING, CONV_SEP, CONVENTIONS


class Station:
    objects: dict[int, set[str]]
    ungatherd_objects: dict[str, int]
    colors: dict[str, list[int]]
    states: dict[int, int]

    def __init__(self, name) -> None:
        self.conf_path = os.path.join(os.path.dirname(__file__), CONVENTIONS)
        self.objects = dict()
        self.colors = dict()
        self.states = dict()

    def fill_dict(self):
        color_handler = ColorRowHandler()
        object_handler = ObjectRowHandler()
        state_handler = StateRowHandler()
        object_handler.setNext(color_handler)
        color_handler.setNext(state_handler)
        with open(self.conf_path, mode='r', encoding=CONV_ENCODING) as fs:
            for raw_line in fs:
                line, _, _ = raw_line.partition(CONV_COMMENT)
                if line:
                    row = line.split(CONV_SEP)
                    if row:
                        object_handler.handle(row, self)
