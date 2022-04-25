from abc import ABC, abstractmethod
import pathlib
from constants import DEF_DESC_PATH, SOURCE_DESC_DIR, SOURCE_DESC_SUFIX
from app.exceptions import DublicateKeyException, UnhandledRowException
from constants import CONV_COMMENT, CONV_ENCODING, CONV_SEP
from logger import get_logger

logger = get_logger(__name__)


class TesterAbstractRowHandler(ABC):

    next_handler: 'TesterAbstractRowHandler' = None

    def __init__(self):
        self.next_handler = None

    @abstractmethod
    def handle(self, row: list[str], tester) -> None:
        if self.next_handler:
            self.next_handler.handle(row, tester)
        else:
            raise UnhandledRowException

    def set_next(self, handler: 'TesterAbstractRowHandler') -> None:
        self.next_handler = handler


class TesterStateRowHandler(TesterAbstractRowHandler):
    def handle(self, row: list[str], tester):
        # state; id
        if len(row) == 2:
            try:
                key = row[0].lower()
                value = int(row[1])
                if key in tester.states:
                    raise DublicateKeyException
                tester.states[key] = value
            except ValueError:
                pass
            else:
                return
        super().handle(row, tester)


class Tester:

    name: str
    states: dict[str, int]

    def __init__(self, name) -> None:
        self.name = name
        self.states = dict()
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
        handler1 = TesterStateRowHandler()
        inner_flag = False
        container: list[tuple[int, str]] = list()

        with open(path, mode='r', encoding=CONV_ENCODING) as fs:
            for line_no, raw_line in enumerate(fs, start=1):
                line, _, _ = raw_line.strip(' \n').partition(CONV_COMMENT)
                if not line:
                    continue
                if line.startswith('['):
                    inner_flag = line.startswith('[Tester]')
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
line [{line_no }]')
            except DublicateKeyException:
                logger.warning(
                    f'Dublicate value for key in the row [{row}] in the \
line [{line_no}]')
            except UnhandledRowException:
                logger.error(
                    f'Couldn`t handle the row [{row}] in the \
line [{line_no}]')
