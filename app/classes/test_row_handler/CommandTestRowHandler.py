from app.classes.TCPClient import TCPClient
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from app.exceptions import BadResponsedMessageException, TCPConnectionError
from app.exceptions import BadSendMessageException
from app.exceptions import FailedTestException
from constants import CMD_PREFIX, RESPONSE_OK_ANSWER

from logger import get_logger

logger = get_logger(__name__)


class CommandTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str],
               client: TCPClient) -> None:

        if len(row) == 3 or len(row) == 4:
            try:
                message = self.get_message_from_row(row)
                client.send(message)
                response = client.receive()
                self.check_response(response, message)
            except (BadResponsedMessageException,
                    BadSendMessageException, TCPConnectionError) as ex:
                raise FailedTestException(ex.message)
        else:
            self.next_handler.handle(
                row, client)

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
        list_request = request.split(':')
        excpected_response = f'{list_request[0]}:\
{list_request[3]}:\
{RESPONSE_OK_ANSWER}'
        if (response != excpected_response):
            message = f'ERROR! Bad response on command [{request}]. \
Expected [{excpected_response}], got [{response}]'
            self.write_test_log_report(message)
            raise BadResponsedMessageException(message)
