from datetime import datetime
import os
from typing import Callable
import shutil
from colorama import Fore

from app.classes.station.Station import Station
from app.classes.test_row_handler.CommandTestRowHandler \
    import CommandTestRowHandler
from app.classes.test_row_handler.StateTestRowHandler \
    import StateTestRowHandler
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
        self.clear_output_dir()

    def run(self, vis_client: Callable) -> bool:
        waiter_handler = WaiterTestRowHandler(self)
        command_handler = CommandTestRowHandler(self)
        state_handler = StateTestRowHandler(self)
        waiter_handler.set_next(command_handler)
        command_handler.set_next(state_handler)
        state_handler.set_next(UnhendledTestRowHandler(self))
        try:
            with open(self.test_path, mode='r', encoding=TEST_ENCODING) as fs:
                try:
                    for line_no, raw_line in enumerate(fs):
                        line, _, _ = raw_line.strip(
                            ' \n').partition(CONV_COMMENT)
                        if line:
                            row = line.split(TEST_FILE_SEP)
                            if row:
                                row = [item.strip(' \n') for item in row]
                                waiter_handler.handle(
                                    row, vis_client)
                except UnicodeDecodeError as ex:
                    self.write_report(self.test_log_path,
                                      f'Test [{self.test_name}] failed. \
Reason [{ex}]')
                    raise FailedTestException()
        except FailedTestException as ex:
            message = f'{self.station.name}::{self.test_name}::\
{Fore.RED}FAILED{Fore.WHITE}::line {line_no} [{line}]. {ex.message}'

            self.write_report(self.test_report_path,
                              f'{self.station.name}::{self.test_name}::\
FAILED{Fore.WHITE}:: line {line_no} [{line}]. {ex.message }')
            print(message)
            return False
        else:
            self.write_report(self.test_report_path,
                              f'{self.test_name}:: {Fore.GREEN}PASSED')
            print(f'{self.test_name}:: {Fore.GREEN}PASSED')
            return True

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
        to_delete_path = os.path.join(os.getcwd(),
                                      OUTPUT_DIR,
                                      self.station.name)

        if (os.path.isdir(to_delete_path)):
            shutil.rmtree(to_delete_path, ignore_errors=True)
