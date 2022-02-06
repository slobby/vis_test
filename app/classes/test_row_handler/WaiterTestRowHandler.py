import time
from typing import Callable
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from logger import get_logger


logger = get_logger(__name__)


class WaiterTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str],
               test_task,
               handler: Callable) -> None:

        if len(row) == 1 and row[0].isdigit():
            self.write_report(
                test_task.test_log_path,
                f'Test [{test_task.test_name}] is waiting for [{row[0]}] sec'
            )
            time.sleep(int(row[0]))
            return
        else:
            self.next_handler.handle(
                row, test_task, handler)
