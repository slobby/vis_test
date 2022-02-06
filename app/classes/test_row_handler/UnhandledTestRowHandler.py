from typing import Callable
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from app.exceptions import UnhandledTestRowException


class UnhendledTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str],
               test_task,
               handler: Callable) -> None:
        raise UnhandledTestRowException
