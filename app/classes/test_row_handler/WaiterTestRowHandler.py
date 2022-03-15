import time
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from app.exceptions import FailedTestException
from logger import get_logger


logger = get_logger(__name__)


class WaiterTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str]) -> None:

        if len(row) == 1 and row[0].isdigit():
            message = f'Wait {row[0]} seconds'
            logger.info(message)
            self.test_task.write_test_log_report(message)
            time.sleep(int(row[0]))
            return
        elif self.next_handler:
            self.next_handler.handle(row)
        else:
            message = 'No next handler'
            raise FailedTestException(message)
