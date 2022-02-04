from app.exceptions import UnhandledRowException
from app.classes.row_handler.AbstractHandler import AbstractRowHandler


class UnhandledRowHandler(AbstractRowHandler):
    def handle(self, row: list[str], station):
        raise UnhandledRowException
