from app.exceptions import DublicateKeyException
from app.classes.row_handler.AbstractHandler import AbstractRowHandler


class ObjectRowHandler(AbstractRowHandler):
    def handle(self, row: list[str], station):
        if len(row) == 2:
            try:
                key = int(row[1])
                val = row[0].lower()
                if key not in station.objects:
                    station.objects[key] = set()
                if val in station.objects[key]:
                    raise DublicateKeyException
                station.objects[key].add(val)
                station.ungatherd_objects[val] = key
            except ValueError:
                pass
            else:
                return
        if self.next_handler:
            self.next_handler.handle(row, station)
