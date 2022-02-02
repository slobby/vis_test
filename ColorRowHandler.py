from AbstractHandler import AbstractRowHandler
from Station import Station


class ColorRowHandler(AbstractRowHandler):
    def handle(self, row: list[str], station: Station):
        if len(row) == 2:
            try:
                key = row[1].strip()
                val = int(row[0].strip())
                if key not in station.colors:
                    station.colors[key] = set()
                station.colors[key].add(val)
            except ValueError:
                pass
            else:
                return
        if next:
            self.next.handle(row, station)
