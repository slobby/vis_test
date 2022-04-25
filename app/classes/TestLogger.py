from datetime import datetime
import os
from abc import ABC, abstractmethod

from constants import OUTPUT_DIR, TEST_ENCODING
from constants import VIS_TEST_VERBOSE, VIS_TEST_VERBOSE_YES

from logger import get_logger


logger = get_logger(__name__)


class AbstractTestLogger(ABC):

    @staticmethod
    @abstractmethod
    def write_report(file_path: str, message: str) -> None:
        pass

    @abstractmethod
    def write_test_log_report(self, message: str) -> None:
        pass

    @abstractmethod
    def write_test_report(self, message: str) -> None:
        pass

    @abstractmethod
    def write_progress_bar(self, message: str) -> None:
        pass


class TestLogger(AbstractTestLogger):
    station_name: str = None
    test_path: str = None
    test_name: str = None
    test_log_path: str = None
    test_report_path: str = None

    def __init__(self, test_path: str, station_name: str, test_name: str):
        self.test_path = test_path
        self.station_name = station_name
        self.test_name = test_name
        self.test_report_path = self._get_test_report_path()
        self.test_log_path = self.test_report_path.replace('.csv', '_log.csv')

    @staticmethod
    def write_report(file_path: str, message: str):
        head, _ = os.path.split(file_path)
        if not os.path.exists(head):
            os.makedirs(head)
        with open(file_path, mode='a+', encoding=TEST_ENCODING) as fs:
            fs.write(message)

    def write_test_log_report(self, message: str) -> None:
        time_stamp = datetime.now().isoformat(sep=' ',
                                              timespec='milliseconds')
        message_to_write = f'[{time_stamp}] - {message}'
        self.write_report(self.test_log_path, message_to_write + '\n')
        if (os.environ.get(VIS_TEST_VERBOSE, 'NO') == VIS_TEST_VERBOSE_YES):
            print(message_to_write)

    def write_test_report(self, message: str) -> None:
        time_stamp = datetime.now().isoformat(sep=' ',
                                              timespec='milliseconds')
        message_to_write = f'[{time_stamp}] - {message}\n'
        self.write_report(self.test_report_path, message_to_write)

    def write_progress_bar(self, message: str) -> None:
        if (os.environ.get(VIS_TEST_VERBOSE, 'NO') != VIS_TEST_VERBOSE_YES):
            print('\033[2K', end='\r', flush=True)
            print(f'{self.test_path}::{self.test_name}::', end='', flush=True)
            print(f'\033[33m{message}', end='\r', flush=True)

    def _get_test_report_path(self):
        _, _, rest = self.test_path.rpartition((self.station_name+os.sep))
        return os.path.join(os.getcwd(),
                            OUTPUT_DIR,
                            self.station_name,
                            rest)
