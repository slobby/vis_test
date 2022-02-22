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
                            message = f'Handle line {line_no} [{line}]'
                            logger.info(message)
                            self.write_test_log_report(message)
                            waiter_handler.handle(row)
        except UnicodeDecodeError:
            # write message if failed due bad encoding
            message = f'{self.test_path}::{self.test_name}::\
FAILED:: Test file encoding is not utf-8'
            message_colored = f'{self.test_path}::{self.test_name}::\
{Fore.RED}FAILED'
            logger.info(message)
            self.write_test_report(message)
            print(message_colored)
            return False
        except FailedTestException as ex:
            # write message if failed
            message = f'{self.test_path}::{self.test_name}::\
FAILED:: line {line_no} [{line}]. {ex.message }'
            message_colored = f'{self.test_path}::{self.test_name}::\
{Fore.RED}FAILED'
            logger.info(message)
            self.write_test_report(message)
            print(message_colored)
            return False
        else:
            # write message if success
            message = f'{self.test_path}::{self.test_name}::PASSED'
            message_colored = f'{self.test_path}::{self.test_name}::\
{Fore.GREEN}PASSED'
            self.write_test_report(message)
            print(message_colored)
            return True
