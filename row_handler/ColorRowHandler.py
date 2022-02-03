from exceptions import DublicateKeyException
from row_handler.AbstractHandler import AbstractRowHandler


class ColorRowHandler(AbstractRowHandler):
    def handle(self, row: list[str], station):
        if len(row) == 2:
            try:
                key = row[1]
                val = int(row[0])
                if key not in station.colors:
                    station.colors[key] = set()
                if val in station.colors[key]:
                    raise DublicateKeyException
                station.colors[key].add(val)
            except ValueError:
                pass
            else:
                return
        if self.next_handler:
            self.next_handler.handle(row, station)
