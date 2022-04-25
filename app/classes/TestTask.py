import os
from abc import ABC, abstractmethod
from colorama import Fore
from app.classes.TCPClient import Clients
from app.classes.TestRowHandler import AbstractTestRowHandler
from constants import CONV_COMMENT, TEST_ENCODING
from app.exceptions import FailedTestException, UnhandledTestRowException
from app.classes.TestLogger import AbstractTestLogger, TestLogger


from logger import get_logger


logger = get_logger(__name__)


class AbstractTestTask(ABC):
    test_path: str
    station_name: str
    row_handler: AbstractTestRowHandler
    clients: Clients
    test_name: str
    test_report_path: str
    test_log_path: str
    test_logger: AbstractTestLogger

    def __init__(self,
                 test_path: str,
                 station_name: str,
                 row_handler: AbstractTestRowHandler,
                 clients: Clients) -> None:
        self.test_path = test_path
        self.station_name = station_name
        self.row_handler = row_handler
        self.clients = clients
        self.test_name = self.get_test_name()
        self.test_logger = TestLogger(
            self.test_path, self.station_name, self.test_name)

    @abstractmethod
    def run(self) -> bool:
        pass

    def get_test_name(self) -> str:
        with open(self.test_path, mode='r', encoding=TEST_ENCODING) as fs:
            first_line = fs.readline()
            if first_line.startswith(CONV_COMMENT):
                _, _, test_name = first_line.partition(CONV_COMMENT)
                return test_name.strip(' \n')
        _, _, rest = self.test_path.rpartition(self.station_name)
        return '_'.join([self.station_name, *rest.split(os.sep)])


class TestTask(AbstractTestTask):

    def __init__(self,
                 test_path: str,
                 station_name: str,
                 row_handler: AbstractTestRowHandler,
                 clients: Clients) -> None:
        super().__init__(test_path, station_name, row_handler, clients)

    def run(self) -> bool:
        result = False
        message_common = f'{self.test_path}::{self.test_name}::'
        try:
            with open(self.test_path, mode='r', encoding=TEST_ENCODING) as fs:
                for line_no, raw_line in enumerate(fs, start=1):
                    raw_line = raw_line.strip(' \n')
                    line, _, _ = raw_line.partition(CONV_COMMENT)
                    if line:
                        log_message = f'Line {line_no} [ {raw_line} ]'
                        logger.info(log_message)
                        self.test_logger.write_test_log_report(log_message)
                        self.test_logger.write_progress_bar(log_message)
                        self.row_handler.handle(
                            line, self.clients, self.test_logger)
        except UnicodeDecodeError:
            # write message if failed due bad encoding
            message = f'{message_common}FAILED:: Test file encoding is not utf-8'
            message_colored = f'{message_common}{Fore.RED}FAILED'
            result = False
        except (FailedTestException, UnhandledTestRowException) as ex:
            # write message if failed
            self.test_logger.write_test_log_report(ex.message)
            message = f'{message_common}FAILED:: line {line_no} [{line}]. {ex.message }'
            message_colored = f'{message_common}{Fore.RED}FAILED'
            result = False
        else:
            # write message if success
            message = f'{message_common}PASSED'
            message_colored = f'{message_common}{Fore.GREEN}PASSED'
            result = True

        if not result:
            logger.info(message)
        self.test_logger.write_test_report(message)
        print('\033[2K', end='\r', flush=True)
        print(message_colored)
        return result
