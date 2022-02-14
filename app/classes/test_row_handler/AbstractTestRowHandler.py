from abc import ABC, abstractmethod
from datetime import datetime
import os
from app.classes.TCPClient import TCPClient

from constants import TEST_ENCODING


class AbstractTestRowHandler(ABC):

    next_handler: 'AbstractTestRowHandler' = None

    def __init__(self, test_task):
        self.test_task = test_task

    @abstractmethod
    def handle(self,
               row: list[str],
               client: TCPClient) -> None:
        pass

    def set_next(self, handler: 'AbstractTestRowHandler') -> None:
        self.next_handler = handler

    def write_report(self, file_path: str, message: str) -> None:
        head, _ = os.path.split(file_path)
        if not os.path.exists(head):
            os.makedirs(head)
        with open(file_path, mode='a+', encoding=TEST_ENCODING) as fs:
            time_stamp = datetime.now().isoformat(sep=' ',
                                                  timespec='milliseconds')
            fs.write(f'[{time_stamp}] ; {message}\n')

    def write_test_log_report(self, message: str) -> None:
        return self.write_report(self.test_task.test_log_path, message)

    def write_test_report(self, message: str) -> None:
        return self.write_report(self.test_task.test_report_path, message)
