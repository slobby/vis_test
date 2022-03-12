from datetime import datetime
import os
from abc import ABC, abstractmethod
from app.classes.TCPClient import TCPClient

from app.classes.station.Station import Station
from constants import CONV_COMMENT, OUTPUT_DIR, TEST_ENCODING
from constants import VIS_TEST_VERBOSE, VIS_TEST_VERBOSE_YES


class TestTask(ABC):
    test_path: str
    station: Station
    name: str
    test_report_path: str
    test_log_path: str

    def __init__(self,
                 test_path: str,
                 station: Station,
                 client: TCPClient) -> None:
        self.test_path = test_path
        self.station = station
        self.client = client
        self.test_name = self.get_test_name()
        self.test_report_path = self.get_test_report_path()
        self.test_log_path = self.get_test_log_path()
        self.clear_output_dir()

    @abstractmethod
    def run(self) -> bool:
        pass

    def get_test_name(self) -> str:
        with open(self.test_path, mode='r', encoding=TEST_ENCODING) as fs:
            first_line = fs.readline()
            if first_line.startswith(CONV_COMMENT):
                _, _, test_name = first_line.partition(CONV_COMMENT)
                return test_name.strip(' \n')
        _, _, rest = self.test_path.rpartition(self.station.name)
        return '_'.join([self.station.name, *rest.split(os.sep)])

    def get_test_report_path(self):
        _, _, rest = self.test_path.rpartition((self.station.name+os.sep))
        return os.path.join(os.getcwd(),
                            OUTPUT_DIR,
                            self.station.name,
                            rest)

    def get_test_log_path(self):
        _, _, rest = self.test_path.rpartition((self.station.name+os.sep))
        return os.path.join(os.getcwd(),
                            OUTPUT_DIR,
                            self.station.name,
                            rest.replace('.csv', '_log.csv'))

    def write_report(self, file_path: str, message: str):
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

    def clear_output_dir(self):
        if os.path.isfile(self.test_report_path):
            os.remove(self.test_report_path)
        if os.path.isfile(self.test_log_path):
            os.remove(self.test_log_path)

    def write_progress_bar(self, message: str) -> None:
        if (os.environ.get(VIS_TEST_VERBOSE, 'NO') != VIS_TEST_VERBOSE_YES):
            print('\033[2K', end='\r', flush=True)
            print(f'{self.test_path}::{self.test_name}::', end='', flush=True)
            print(f'\033[33m{message}', end='\r', flush=True)
