from app.classes.color.Color import LayerColor
from app.classes.test_row_handler.AbstractTestRowHandler \
    import AbstractTestRowHandler
from app.exceptions import BadResponsedMessageException, TCPConnectionError
from app.exceptions import BadSendMessageException
from app.exceptions import FailedTestException
from constants import COLORS_SEP, GET_PREFIX, RESPONSE_ERROR_ANSWER
from constants import RESPONSE_NO_ANSWER

from logger import get_logger

logger = get_logger(__name__)


class StateTestRowHandler(AbstractTestRowHandler):

    def handle(self,
               row: list[str]) -> None:
        if len(row) == 2 and (';' in row[1]):
            try:
                message = self.get_message_from_row(row)
                self.test_task.client.send(message)
                self.test_task.write_test_log_report(
                    f'Send message [{message}]')
                response = self.test_task.client.receive()
                self.test_task.write_test_log_report(
                    f'Receive message [{response}]')
                self.check_response(response, row)
            except (BadResponsedMessageException,
                    BadSendMessageException, TCPConnectionError) as ex:
                raise FailedTestException(ex.message)
        elif self.next_handler:
            self.next_handler.handle(row)
        else:
            message = 'No next handler'
            FailedTestException(message)

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
            self.test_task.write_test_log_report(message)
            raise BadSendMessageException(message)
        if id_object not in self.test_task.station.states:
            message = f'ERROR! Couldn`t object [{alias_object}] in states'
            self.test_task.write_test_log_report(message)
            raise BadSendMessageException(message)
        if (state not in self.test_task.station.states[id_object]):
            message = f'ERROR! Couldn`t find state [{state}] for object [{alias_object}] \
in station model [{self.test_task.station.name}]'
            self.test_task.write_test_log_report(message)
            raise BadSendMessageException(message)
        return f'{GET_PREFIX}:{id_object}:{name_object}'

    def check_response(self,
                       response: str,
                       row: list[str]) -> None:
        if response == RESPONSE_ERROR_ANSWER or \
                response.endswith(RESPONSE_NO_ANSWER):
            message = f'ERROR! Got bad responce [{response}]'
            self.test_task.write_test_log_report(message)
            raise BadResponsedMessageException(message)
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
                self.test_task.write_test_log_report(message)
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
                self.test_task.write_test_log_report(message)
                raise BadResponsedMessageException(message)

            layer_color = LayerColor(blink_color, permanent_color)
            layers[layer] = layer_color
        if id_object not in self.test_task.station.states:
            message = f'ERROR! Couldn`t find object [{id_object}] \
in station.objects'
            self.test_task.write_test_log_report(message)
            raise BadResponsedMessageException(message)
        for lr in self.test_task.station.states[id_object][state]:
            if lr not in layers:
                message = f'ERROR! Couldn`t find layer [{lr}] \
in station.states for state [{state}]'
                self.test_task.write_test_log_report(message)
                raise BadResponsedMessageException(message)
            if layers[lr] != (
                    self.test_task.station.states[id_object][state][lr]):
                message = f'ERROR! For \
objects [{self.test_task.station.objects[id_object]}] in \
state [{state}] \
for layer [{lr}] expected state \
is [{self.test_task.station.states[id_object][state][lr].blink_color}: \
{self.test_task.station.states[id_object][state][lr].permanent_color}], \
got [{layers[lr].blink_color}: \
{layers[lr].permanent_color}]'
                self.test_task.write_test_log_report(message)
                raise BadResponsedMessageException(message)
