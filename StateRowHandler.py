from AbstractHandler import AbstractRowHandler
from Station import Station


class StateRowHandler(AbstractRowHandler):
    def handle(self, row: list[str], stattion: Station):
        # id; state; layer; color [colorm, color]
        if len(row) == 4:
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
