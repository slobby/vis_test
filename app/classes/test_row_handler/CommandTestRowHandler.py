import socket
from typing import Callable
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
                    f'Send message [{message}] to visualisation'
                )
                response = vis_client(message)
                self.write_test_log_report(
                    f'Recive message [{response}] from visualisation'
                )
                self.check_response(response, message)
            except (BadResponsedMessageException,
                    BadSendMessageException) as ex:
                raise FailedTestException(ex.massage)
            except (ConnectionRefusedError, socket.timeout) as ex:
                self.write_test_log_report(
                    f'ERROR! While sending message to visualisation [{ex}]')
                raise FailedTestException()
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
            message = f'ERROR! Couldn`t find object [{alias_object}] \
in station model [{self.test_task.station.name}]'
            self.write_test_log_report(message)
            raise BadSendMessageException(message)
        if type_command not in '012':
            message = f'ERROR! Wrong command type [{type_command}]'
            self.write_test_log_report(message)
            raise BadSendMessageException(message)
        return f'{CMD_PREFIX}:{id_object}:\
{name_object}:{name_command}:{type_command}'

    def check_response(self, response: str, request: str) -> None:
        request = request.split(':')
        excpected_response = f'{request[0]}:\
{request[3]}:\
{RESPONSE_OK_ANSWER}'
        if (response != excpected_response):
            message = self.write_test_log_report(
                f'ERROR! Bad response on command [{request}]. \
Expected [{excpected_response}], got [{response}]')
            raise BadResponsedMessageException(message)
