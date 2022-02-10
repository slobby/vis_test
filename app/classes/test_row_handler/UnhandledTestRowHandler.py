from typing import Callable
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from app.exceptions import FailedTestException


class UnhendledTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str],
               handler: Callable) -> None:
        message = f'ERROR! Couldn`t parse input string [{row}]'
        self.write_test_log_report(message)
        raise FailedTestException(message)
