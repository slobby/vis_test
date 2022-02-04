from pprint import pprint
from app.classes.station.Station import Station


if __name__ == '__main__':
    station = Station("test")
    pprint(station.objects)
    pprint(station.ungatherd_objects)
    pprint(station.colors)
    pprint(station.states)
