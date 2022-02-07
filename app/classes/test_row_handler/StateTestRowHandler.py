import socket
from typing import Callable
from xmlrpc.client import Boolean
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from app.exceptions import BadResponsedMessageException
from app.exceptions import BadSendMessageException
from app.exceptions import FailedTestException
from constants import GET_PREFIX, RESPONSE_ERROR_ANSWER, RESPONSE_NO_ANSWER, RESPONSE_OK_ANSWER

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

    def is_successful_response(self, response: str,  row: list[str]) -> Boolean:
        if response == RESPONSE_ERROR_ANSWER or response.endswith(RESPONSE_NO_ANSWER):
            return False
        response_items = response.split(':')
        id_object = int(response_items[0])
        state = row[1].lower()

            layer = int(row[2])
             colors = row[3].split(COLORS_SEP)
              colors = [item.strip().lower() for item in colors]
               if len(colors) != 2:
                    raise ValueError
                if colors[1] == '':
                    colors.reverse()
                    colors[0] = colors[1]
                layer_color = LayerColor(*colors)
                if id not in station.objects or \
                        layer_color.blink_color not in station.colors or \
                        layer_color.permanent_color not in station.colors:
                    raise NotFoundKeyException

        excpected_response = f'{message_items[0]}:\
{message_items[3]}:\
{RESPONSE_OK_ANSWER}'
        if (response != excpected_response):
            self.write_test_log_report(
                f'Erorr! Bad response on command [{message}]. \
Expected [{excpected_response}], got [{response}]')
            return False
        return True
