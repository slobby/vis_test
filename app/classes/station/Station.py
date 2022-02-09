import pathlib
from app.classes.color.Color import LayerColor
from constants import DEF_DESC_PATH, SOURCE_DESC_DIR, SOURCE_DESC_SUFIX
from app.exceptions import DublicateKeyException
from app.exceptions import DublicateLayerException
from app.exceptions import UnhandledRowException
from app.classes.row_handler.ColorRowHandler import ColorRowHandler
from app.classes.row_handler.ObjectRowHandler import ObjectRowHandler
from app.classes.row_handler.StateRowHandler import StateRowHandler
from app.classes.row_handler.UnhandledRowHandler import UnhandledRowHandler
from constants import CONV_COMMENT, CONV_ENCODING, CONV_SEP
from logger import get_logger

logger = get_logger(__name__)


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
        color_handler = ColorRowHandler()
        object_handler = ObjectRowHandler()
        state_handler = StateRowHandler()
        object_handler.set_next(color_handler)
        color_handler.set_next(state_handler)
        state_handler.set_next(UnhandledRowHandler())

        with open(path, mode='r', encoding=CONV_ENCODING) as fs:
            for line_no, raw_line in enumerate(fs):
                line, _, _ = raw_line.strip(' \n').partition(CONV_COMMENT)
                if line:
                    row = line.split(CONV_SEP)
                    try:
                        if row:
                            row = [item.strip(' \n') for item in row]
                            object_handler.handle(row, self)
                    except (ValueError, KeyError):
                        logger.error(
                            f'Error while parsing the row [{row}] in the \
line [{line_no + 1}]')
                    except DublicateKeyException:
                        logger.warning(
                            f'Dublicate value for key in the row [{row}] in the \
line [{line_no + 1}]')
                    except DublicateLayerException:
                        logger.warning(
                            f'Dublicate layer in the row [{row}] in the \
line [{line_no + 1}]')
                    except UnhandledRowException:
                        logger.error(
                            f'Couldn`t handle the row [{row}] in the \
line [{line_no + 1}]')
