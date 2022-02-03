from audioop import reverse
from color.Color import LayerColor
from constants import COLORS_SEP
from row_handler.AbstractHandler import AbstractRowHandler


class StateRowHandler(AbstractRowHandler):
    def handle(self, row: list[str], station):
        # id; state; layer; color [colorm, color]
        if len(row) == 4:
            try:
                id = int(row[0])
                state = row[1]
                layer = int(row[2])
                colors = row[3].split(COLORS_SEP)
                colors = [item.strip() for item in colors]
                if len(colors) != 2:
                    raise ValueError
                if colors[1] == '':
                    colors.reverse()
                    colors[0] = colors[1]
                layer_color = LayerColor(*colors)
                if id not in station.objects or \
                        layer_color.blink_color not in station.colors or \
                        layer_color.permanent_color not in station.colors:
                    raise KeyError
                if id not in station.states:
                    station.states[id] = dict()
                if state not in station.states[id]:
                    station.states[id][state] = dict()
                if layer in station.states[id][state]:
                    raise KeyError
                station.states[id][state][layer] = layer_color
            except ValueError:
                pass
            else:
                return
        if self.next_handler:
            self.next_handler.handle(row, station)
