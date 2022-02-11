from datetime import datetime
import os
from typing import Callable
from abc import ABC, abstractmethod

from app.classes.station.Station import Station
from constants import CONV_COMMENT, OUTPUT_DIR, TEST_ENCODING


class TestTask(ABC):
    test_path: str
    station: Station
    name: str
    test_report_path: str
    test_log_path: str

    def __init__(self, test_path: str, station: Station) -> None:
        self.test_path = test_path
        self.station = station
        self.test_name = self.get_test_name()
        self.test_report_path = self.get_test_report_path()
        self.test_log_path = self.get_test_log_path()
        self.clear_output_dir()

    @abstractmethod
    def run(self, vis_client: Callable) -> bool:
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
        with open(file_path, mode='a', encoding=TEST_ENCODING) as fs:
            time_stamp = datetime.now().isoformat(sep=' ',
                                                  timespec='milliseconds')
            fs.write(f'[{time_stamp}] ; {message}\n')

    def clear_output_dir(self):
        if os.path.isfile(self.test_report_path):
            os.remove(self.test_report_path)
        if os.path.isfile(self.test_log_path):
            os.remove(self.test_log_path)
