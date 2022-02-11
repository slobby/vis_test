import socket
from typing import Callable
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
                    f'Send message [{message}] to visualisation'
                )
                response = vis_client(message)
                self.write_test_log_report(
                    f'Recive message [{response}] from visualisation'
                )
                self.check_response(response, row)
            except (BadResponsedMessageException,
                    BadSendMessageException) as ex:
                raise FailedTestException(ex.message)
            except (ConnectionRefusedError, socket.timeout) as ex:
                self.write_test_log_report(
                    f'ERROR! While sending message to visualisation [{ex}]')
                raise FailedTestException(f'{ex}')
        else:
            self.next_handler.handle(
                row, vis_client)

    def get_message_from_row(self, row: list[str]) -> str:
        alias_object = row[0]
        name_object, _, state = row[1].partition(';')
        if (alias_object in
            self.test_task.station.ungatherd_objects and
                self.test_task.station.ungatherd_objects[alias_object] in
                self.test_task.station.objects):
            id_object = self.test_task.station.ungatherd_objects[alias_object]
        else:
            message = f'ERROR! Couldn`t find object [{alias_object}] \
in station model [{self.test_task.station.name}]'
            self.write_test_log_report(message)
            raise BadSendMessageException(message)
        if (state not in self.test_task.station.states[id_object]):
            message = f'ERROR! Couldn`t find state [{state}] for object [{alias_object}] \
in station model [{self.test_task.station.name}]'
            self.write_test_log_report(message)
            raise BadSendMessageException(message)
        return f'{GET_PREFIX}:{id_object}:{name_object}'

    def check_response(self,
                       response: str,
                       row: list[str]) -> None:
        if response == RESPONSE_ERROR_ANSWER or \
                response.endswith(RESPONSE_NO_ANSWER):
            self.write_test_log_report(
                f'ERROR! Got bad responce [{response}]')
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
                message = f'ERROR! Got wrong amount of \
object`s colors [{len(items)}]'
                self.write_test_log_report(message)
                raise BadResponsedMessageException(message)

            for color, value in self.test_task.station.colors.items():
                if id_permanent_color in value:
                    permanent_color = color
                    break
            for color, value in self.test_task.station.colors.items():
                if id_blink_color in value:
                    blink_color = color
                    break
            if not permanent_color or not blink_color:
                message = f'ERROR! Couldn`t find color [{id_permanent_color}] \
 or [{id_blink_color}] in station.colors'
                self.write_test_log_report(message)
                raise BadResponsedMessageException(message)

            layer_color = LayerColor(blink_color, permanent_color)
            layers[layer] = layer_color
        if id_object not in self.test_task.station.states:
            message = f'ERROR! Couldn`t find object [{id_object}] \
in station.objects'
            self.write_test_log_report(message)
            raise BadResponsedMessageException(message)
        for lr in self.test_task.station.states[id_object][state]:
            if lr not in layers:
                message = f'ERROR! Couldn`t find layer [{lr}] \
in station.states for state [{state}]'
                self.write_test_log_report(message)
                raise BadResponsedMessageException(message)
            if layers[lr] != (
                    self.test_task.station.states[id_object][state][lr]):
                message = f'ERROR! For \
objects [{self.test_task.station.objects[id_object]}] in \
state [{state}] \
for layer [{lr}] expected state \
is [{self.test_task.station.states[id_object][state][lr]}], \
got [{layers[lr]}]'
                self.write_test_log_report(message)
                raise BadResponsedMessageException(message)
