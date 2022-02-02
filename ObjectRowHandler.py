from AbstractHandler import AbstractRowHandler
from Station import Station


class ObjectRowHandler(AbstractRowHandler):
    def handle(self, row: list[str], station: Station):
        if len(row) == 2:
            try:
                key = int(row[1].strip())
                val = row[0].strip()
                if key not in station.objects:
                    station.objects[key] = set()
                station.objects[key].add(val)
                station.ungatherd_objects[val] = key
            except ValueError:
                pass
            else:
                return
        if next:
            self.next.handle(row, station)
