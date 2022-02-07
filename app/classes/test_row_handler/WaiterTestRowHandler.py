import time
from typing import Callable
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from logger import get_logger


logger = get_logger(__name__)


class WaiterTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str],
               vis_client: Callable) -> None:

        if len(row) == 1 and row[0].isdigit():
            self.write_test_log_report(
                f'Waiting for [{row[0]}] sec')
            time.sleep(int(row[0]))
            return
        else:
            self.next_handler.handle(
                row, vis_client)
