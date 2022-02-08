from typing import Callable
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from app.exceptions import FailedTestException


class UnhendledTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str],
               handler: Callable) -> None:
        raise FailedTestException
