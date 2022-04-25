from abc import ABC, abstractmethod
import pathlib
from collections import namedtuple
from constants import COLORS_SEP, DEF_DESC_PATH, SOURCE_DESC_DIR, SOURCE_DESC_SUFIX
from app.exceptions import DublicateKeyException, DublicateLayerException
from app.exceptions import UnhandledRowException, NotFoundKeyException
from constants import CONV_COMMENT, CONV_ENCODING, CONV_SEP
from logger import get_logger

logger = get_logger(__name__)


LayerColor = namedtuple("LayerColor", "blink_color permanent_color")


class StationAbstractRowHandler(ABC):

    next_handler: 'StationAbstractRowHandler' = None

    def __init__(self):
        self.next_handler = None

    @abstractmethod
    def handle(self, row: list[str], station) -> None:
        if self.next_handler:
            self.next_handler.handle(row, station)
        else:
            raise UnhandledRowException

    def set_next(self, handler: 'StationAbstractRowHandler') -> None:
        self.next_handler = handler


class StationColorRowHandler(StationAbstractRowHandler):
    def handle(self, row: list[str], station):
        if len(row) == 2:
            try:
                key = row[1].lower()
                val = int(row[0])
                if key not in station.colors:
                    station.colors[key] = set()
                if val in station.colors[key]:
                    raise DublicateKeyException
                station.colors[key].add(val)
            except ValueError:
                pass
            else:
                return
        super().handle(row, station)


class StationObjectRowHandler(StationAbstractRowHandler):
    def handle(self, row: list[str], station):
        if len(row) == 2:
            try:
                key = int(row[1])
                val = row[0].lower()
                if key not in station.objects:
                    station.objects[key] = set()
                if val in station.objects[key]:
                    raise DublicateKeyException
                station.objects[key].add(val)
                station.ungatherd_objects[val] = key
            except ValueError:
                pass
            else:
                return
        super().handle(row, station)


class StationStateRowHandler(StationAbstractRowHandler):
    def handle(self, row: list[str], station):
        # id; state; layer; color [colorm, color]
        if len(row) == 4:
            try:
                id = int(row[0])
                state = row[1].lower()
                layer = int(row[2])
                colors = row[3].split(COLORS_SEP)
                colors = [item.strip().lower() for item in colors]
                if len(colors) != 2:
                    raise ValueError
                if colors[1] == '':
                    colors.reverse()
                    colors[0] = colors[1]
                layer_color = LayerColor(*colors)
                if id not in station.objects or \
                        layer_color.blink_color not in station.colors or \
                        layer_color.permanent_color not in station.colors:
                    raise NotFoundKeyException
                if id not in station.states:
                    station.states[id] = dict()
                if state not in station.states[id]:
                    station.states[id][state] = dict()
                if layer in station.states[id][state]:
                    raise DublicateLayerException
                station.states[id][state][layer] = layer_color
            except ValueError:
                pass
            else:
                return
        super().handle(row, station)


class Station:

    name: str
    objects: dict[int, set[str]]
    ungatherd_objects: dict[str, int]
    colors: dict[str, set[int]]
    states: dict[int, dict[str, dict[int, LayerColor]]]

    def __init__(self, name) -> None:
        self.name = name
        self.objects = dict()
        self.colors = dict()
        self.states = dict()
        self.ungatherd_objects = dict()
        def_conf_file_path = pathlib.Path.joinpath(pathlib.Path.cwd(),
                                                   DEF_DESC_PATH)
        station_file_path = pathlib.Path.joinpath(pathlib.Path.cwd(),
                                                  SOURCE_DESC_DIR,
                                                  self.name,
                                                  SOURCE_DESC_SUFIX)
        for file_path in [def_conf_file_path, station_file_path]:
            if pathlib.Path.is_file(file_path):
                self.fill_dict(file_path)

    def fill_dict(self, path):
        handler1 = StationColorRowHandler()
        handler2 = StationObjectRowHandler()
        handler3 = StationStateRowHandler()
        handler1.set_next(handler2)
        handler2.set_next(handler3)
        inner_flag = False
        container: list[tuple[int, str]] = list()

        with open(path, mode='r', encoding=CONV_ENCODING) as fs:
            for line_no, raw_line in enumerate(fs, start=1):
                line, _, _ = raw_line.strip(' \n').partition(CONV_COMMENT)
                if not line:
                    continue
                if line.startswith('['):
                    inner_flag = line.startswith('[Visualisation]')
                    continue
                if inner_flag:
                    container.append((line_no, line))

        for line_no, line in container:
            row = line.split(CONV_SEP)
            try:
                if row:
                    row = [item.strip(' \n') for item in row]
                    handler1.handle(row, self)
            except (ValueError, KeyError):
                logger.error(
                    f'Error while parsing the row [{row}] in the \
line [{line_no}]')
            except DublicateKeyException:
                logger.warning(
                    f'Dublicate value for key in the row [{row}] in the \
line [{line_no}]')
            except DublicateLayerException:
                logger.warning(
                    f'Dublicate layer in the row [{row}] in the \
line [{line_no}]')
            except UnhandledRowException:
                logger.error(
                    f'Couldn`t handle the row [{row}] in the \
line [{line_no}]')
