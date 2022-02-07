import socket
from typing import Callable
from xmlrpc.client import Boolean
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from app.exceptions import BadResponsedMessageException
from app.exceptions import BadSendMessageException
from app.exceptions import FailedTestException
from constants import CMD_PREFIX, RESPONSE_OK_ANSWER

from logger import get_logger

logger = get_logger(__name__)


class CommandTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str],
               vis_client: Callable) -> None:
        if len(row) == 3 or len(row) == 4:
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
                if not self.is_successful_response(response, message):
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
        name_object = row[1]
        name_command = row[2]
        type_command = row[3] if len(row) == 4 else '0'
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
        if type_command not in '012':
            raise BadSendMessageException
        return f'{CMD_PREFIX}:{id_object}:\
{name_object}:{name_command}:{type_command}'

    def is_successful_response(self, response: str, message: str) -> Boolean:
        message_items = message.split(':')
        excpected_response = f'{message_items[0]}:\
{message_items[3]}:\
{RESPONSE_OK_ANSWER}'
        if (response != excpected_response):
            self.write_test_log_report(
                f'Erorr! Bad response on command [{message}]. \
Expected [{excpected_response}], got [{response}]')
            return False
        return True
