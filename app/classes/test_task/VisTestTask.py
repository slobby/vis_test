from typing import Callable
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
from app.classes.test_task.TestTask import TestTask
from app.exceptions import FailedTestException
from constants import CONV_COMMENT, TEST_ENCODING, TEST_FILE_SEP


class VisTestTask(TestTask):

    def __init__(self, test_path: str, station: Station) -> None:
        super().__init__(test_path, station)

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
