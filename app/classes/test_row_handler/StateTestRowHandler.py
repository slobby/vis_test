import socket
from typing import Callable
from xmlrpc.client import Boolean
from app.classes.color.Color import LayerColor
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from app.exceptions import BadResponsedMessageException
from app.exceptions import BadSendMessageException
from app.exceptions import FailedTestException
from constants import COLORS_SEP, GET_PREFIX, RESPONSE_ERROR_ANSWER
from constants import RESPONSE_NO_ANSWER

from logger import get_logger

logger = get_logger(__name__)


class StateTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str],
               vis_client: Callable) -> None:
        if len(row) == 2 and (';' in row[1]):
            try:
                message = self.get_message_from_row(row)
                self.write_test_log_report(
                    f'Test [{self.test_task.test_name}] \
send message [{message}] to visualisation'
                )
                response = vis_client(message)
                self.write_test_log_report(
                    f'Test [{self.test_task.test_name}] \
recive message [{response}] from visualisation'
                )
                if not self.is_successful_response(response, row):
                    raise BadResponsedMessageException
            except (BadResponsedMessageException, BadSendMessageException):
                raise FailedTestException
            except (ConnectionRefusedError, socket.timeout) as ex:
                self.write_test_log_report(
                    f'Erorr! While sending message to visualisation [{ex}]')
                raise FailedTestException
        else:
            self.next_handler.handle(
                row, vis_client)

    def get_message_from_row(self, row: list[str]) -> str:
        alias_object = row[0]
        name_object, _, _ = row[1].partition(';')
        if (alias_object in
            self.test_task.station.ungatherd_objects and
                self.test_task.station.ungatherd_objects[alias_object] in
                self.test_task.station.objects):
            id_object = self.test_task.station.ungatherd_objects[alias_object]
        else:
            self.write_test_log_report(
                f'Erorr! Couldn`t find object [{alias_object}] \
in station [{self.test_task.station.name}] model')
            raise BadSendMessageException
        return f'{GET_PREFIX}:{id_object}:{name_object}'

    def is_successful_response(self,
                               response: str,
                               row: list[str]) -> Boolean:
        if response == RESPONSE_ERROR_ANSWER or \
                response.endswith(RESPONSE_NO_ANSWER):
            return False
        response_items = response.split(':')
        id_object = int(response_items[0])
        _, _, raw_state = row[1].partition(';')
        state = raw_state.lower().strip()
        layers = dict()
        for record in response_items[2:]:
            items = record.split(COLORS_SEP)
            layer = int(items[0])
            permanent_color = None
            blink_color = None
            if len(items) == 2:
                id_permanent_color = int(items[1])
                id_blink_color = int(items[1])
            elif len(items) == 3:
                id_permanent_color = int(items[2])
                id_blink_color = int(items[1])
            else:
                return False

            for color, value in self.test_task.station.colors.items():
                if id_permanent_color in value:
                    permanent_color = color
                    break
            for color, value in self.test_task.station.colors.items():
                if id_blink_color in value:
                    blink_color = color
                    break
            if not permanent_color or not blink_color:
                return False

            layer_color = LayerColor(blink_color, permanent_color)
            layers[layer] = layer_color
        if id_object not in self.test_task.station.states:
            return False
        for lr in self.test_task.station.states[id_object][state]:
            if lr not in layers:
                return False
            if layers[lr] != self.test_task. \
                    station.states[id_object][state][lr]:
                return False
        return True
