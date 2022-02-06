from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable

from constants import TEST_ENCODING


class AbstractTestRowHandler(ABC):

    next_handler: 'AbstractTestRowHandler' = None

    @abstractmethod
    def handle(self,
               row: list[str],
               test_task,
               handler: Callable) -> None:
        pass

    def set_next(self, handler: 'AbstractTestRowHandler') -> None:
        self.next_handler = handler

    def write_report(self, file_path: str, message: str):
        with open(file_path, mode='a+', encoding=TEST_ENCODING) as fs:
            time_stamp = datetime.now().isoformat(sep=' ',
                                                  timespec='milliseconds')
            fs.write(f'[{time_stamp}] ; {message}')
