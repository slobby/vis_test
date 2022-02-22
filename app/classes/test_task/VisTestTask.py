from colorama import Fore
from app.classes.TCPClient import TCPClient

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
from logger import get_logger


logger = get_logger(__name__)


class VisTestTask(TestTask):

    def __init__(self,
                 test_path: str,
                 station: Station,
                 client: TCPClient) -> None:
        super().__init__(test_path, station, client)

    def run(self) -> bool:
        waiter_handler = WaiterTestRowHandler(self)
        command_handler = CommandTestRowHandler(self)
        state_handler = StateTestRowHandler(self)
        waiter_handler.set_next(command_handler)
        command_handler.set_next(state_handler)
        state_handler.set_next(UnhendledTestRowHandler(self))
        try:
            with open(self.test_path, mode='r', encoding=TEST_ENCODING) as fs:
                for line_no, raw_line in enumerate(fs, start=1):
                    line, _, _ = raw_line.strip(
                        ' \n').partition(CONV_COMMENT)
                    if line:
                        row = line.split(TEST_FILE_SEP)
                        if row:
                            row = [item.strip(' \n') for item in row]
                            waiter_handler.handle(row)
        except UnicodeDecodeError:
            message = f'{self.station.name}::{self.test_name}::\
FAILED::Bad encoding in test file'
            self.write_report(self.test_report_path, message)
            logger.info(message)
            print(f'{self.station.name}::{self.test_name}::\
{Fore.RED}FAILED{Fore.WHITE}::Bad encoding in test file')
            return False
        except FailedTestException as ex:
            message = f'{self.station.name}::{self.test_name}::\
FAILED:: line {line_no} [{line}]. {ex.message }'
            logger.info(message)
            self.write_report(self.test_report_path, message)
            print(f'{self.station.name}::{self.test_name}::\
{Fore.RED}FAILED{Fore.WHITE}::line {line_no} [{line}]. {ex.message}')
            return False
        else:
            message = f'{self.test_name}:: {Fore.GREEN}PASSED'
            self.write_report(self.test_report_path, message)
            print(message)
            return True
