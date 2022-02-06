from typing import Callable
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from app.exceptions import BadResponseExcpetion, FailedTestException

from logger import get_logger

logger = get_logger(__name__)


class CommandTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str],
               test_task,
               handler: Callable) -> None:
        if len(row) == 3 and len(row) == 4:
            try:
                message = self.get_message_from_row(row)
                self.write_report(
                    test_task.test_log_path,
                    f'Test [{test_task.test_name}] \
    send message [{message}] to visualisation'
                )
                response = handler(message)
                self.write_report(
                    test_task.test_log_path,
                    f'Test [{test_task.test_name}] \
    recive message [{response}] from visualisation'
                )
                if not self.is_successful_response(response, message):
                    raise BadResponseExcpetion
            except BadResponseExcpetion:
                raise FailedTestException

        else:
            self.next_handler.handle(
                row, test_task, handler)
