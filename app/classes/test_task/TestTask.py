import datetime
import os
from typing import Callable

from app.classes.client import send_and_recieve
from app.classes.station.Station import Station
from app.classes.test_row_handler.CommandTestRowHandler \
    import CommandTestRowHandler
from app.classes.test_row_handler.UnhandledTestRowHandler \
    import UnhendledTestRowHandler
from app.classes.test_row_handler.WaiterTestRowHandler \
    import WaiterTestRowHandler
from app.exceptions import FailedTestException
from constants import CONV_COMMENT, OUTPUT_DIR, TEST_ENCODING, TEST_FILE_SEP


class TestTask:
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

    def run(self, handler: Callable) -> None:
        waiter_handler = WaiterTestRowHandler()
        command_handler = CommandTestRowHandler()
        # state_handler = StateTestRowHandler()
        waiter_handler.set_next(command_handler)
        command_handler.set_next(UnhendledTestRowHandler())
        # state_handler.set_next(UnhandledTestRowHandler())
        with open(self.test_path, mode='r', encoding=TEST_ENCODING) as fs:
            for line_no, raw_line in enumerate(fs):
                line, _, _ = raw_line.strip(' \n').partition(CONV_COMMENT)
                if line:
                    row = line.split(TEST_FILE_SEP)
                    try:
                        if row:
                            row = [item.strip(' \n') for item in row]
                            waiter_handler.handle(
                                row, self, send_and_recieve)
                    except FailedTestException:
                        self.write_report(self.test_report_path,
                                          f'Test [{self.test_name}] failed. \
Details - look [{self.test_log_path} file]')

    def get_test_name(self) -> str:
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
        with open(file_path, mode='a', encoding=TEST_ENCODING) as fs:
            time_stamp = datetime.now().isoformat(sep=' ',
                                                  timespec='milliseconds')
            fs.write(f'[{time_stamp}] ; {message}')
