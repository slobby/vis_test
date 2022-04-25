from abc import ABC, abstractmethod
import datetime
import time
from app.classes.Station import LayerColor, Station
from app.classes.TCPClient import Clients
from app.classes.TestLogger import AbstractTestLogger
from app.classes.Tester import Tester

from app.exceptions import BadResponsedMessageException, BadSendMessageException
from app.exceptions import FailedTestException, TCPConnectionError, UnhandledTestRowException
# , FailedTestException
from constants import CMD_PREFIX, COLORS_SEP, COMMAND_SEP, DELTA_TIME, GET_PREFIX, RESPONSE_SEP
from constants import MARKER_ELAPSED_TIME, MARKER_SEP, MARKER_TESTER, MARKER_VIS
from constants import PARAM_SEP, RESPONSE_ERROR_ANSWER, RESPONSE_NO_ANSWER

from logger import get_logger

logger = get_logger(__name__)


class AbstractTestRowHandler(ABC):

    next_handler: 'AbstractTestRowHandler' = None

    def __init__(self):
        self.next_handler = None

    @abstractmethod
    def handle(self, line: str, clients: Clients, test_logger: AbstractTestLogger) -> None:
        if self.next_handler:
            self.next_handler.handle(line, clients, test_logger)
        else:
            message = f'ERROR! Couldn`t parse input string [{line}]'
            raise UnhandledTestRowException(message)

    def set_next(self, handler: 'AbstractTestRowHandler') -> None:
        self.next_handler = handler


class WaiterTestRowHandler(AbstractTestRowHandler):

    def handle(self, line: str, clients: Clients,  test_logger: AbstractTestLogger) -> None:

        if line.isdigit():
            message = f'Wait {line} seconds'
            logger.info(message)
            time.sleep(int(line))
        else:
            super().handle(line, clients, test_logger)


class VisTestRowHandler(AbstractTestRowHandler):

    def __init__(self, station: Station):
        self.station = station
        super().__init__()

    def handle(self, line: str, clients: Clients,  test_logger: AbstractTestLogger) -> None:
        marker, marker_sep, tail = line.partition(MARKER_SEP)
        if marker_sep and marker == MARKER_VIS:
            try:
                params = [item.strip() for item in tail.split(PARAM_SEP)]
                params_length = len(params)
                if params_length == 6:
                    self.handle_state(params, clients, test_logger)
                elif params_length == 5:
                    self.handle_command(params, clients, test_logger)
                else:
                    message = f'ERROR! For Visualisation record [{line}] wrong params quantities [{params_length}]]'
                    raise BadSendMessageException(message)
            except (BadResponsedMessageException,
                    BadSendMessageException, TCPConnectionError) as ex:
                raise FailedTestException(ex.message)
        else:
            super().handle(line, clients, test_logger)

    def handle_state(self, params: list[str], clients: Clients, test_logger: AbstractTestLogger) -> None:
        TCP_id, station_id, station_sub_id, object_type_name, object_name, object_state_raw = params
        object_state, elapsed_sep, time_elapsed = object_state_raw.partition(
            MARKER_ELAPSED_TIME)

        TCP_client = clients.get_by_name(TCP_id)
        request = self.get_state_request(
            station_id, station_sub_id, object_type_name, object_name, object_state)

        if elapsed_sep:
            delta_time = DELTA_TIME
            if time_elapsed:
                try:
                    delta_time = int(time_elapsed)
                except (ValueError, TypeError):
                    raise BadSendMessageException(
                        f'ERROR! Couldn`t convert string [{time_elapsed}] in integer')
            finish_time = datetime.datetime.now() + datetime.timedelta(seconds=delta_time)

            while (datetime.datetime.now() < finish_time):
                try:
                    TCP_client.send(request)
                    test_logger.write_test_log_report(
                        f'Send to client [{TCP_client.alias}] message [{request}]')
                    response = TCP_client.receive()
                    test_logger.write_test_log_report(
                        f'Receive from client [{TCP_client.alias}] message [{response}]')
                    self.check_state_response(response, object_state)
                except (BadResponsedMessageException) as ex:
                    test_logger.write_test_log_report(ex.message)
                    time.sleep(1)
                else:
                    return None

        TCP_client.send(request)
        test_logger.write_test_log_report(
            f'Send to client [{TCP_client.alias}] message [{request}]')
        response = TCP_client.receive()
        test_logger.write_test_log_report(
            f'Receive from client [{TCP_client.alias}] message [{response}]')
        self.check_state_response(response, object_state)

    def handle_command(self, params: list[str], clients: Clients, test_logger: AbstractTestLogger) -> None:
        TCP_id, station_id, object_type_name, object_name, command_name_raw = params
        command_name, _, command_type = command_name_raw.partition(
            COMMAND_SEP)

        TCP_client = clients.get_by_name(TCP_id)
        request = self.get_command_request(
            station_id, object_type_name, object_name, command_name, command_type)
        TCP_client.send(request)
        test_logger.write_test_log_report(
            f'Send to client [{TCP_client.alias}] message [{request}]')
        response = TCP_client.receive()
        test_logger.write_test_log_report(
            f'Receive from client [{TCP_client.alias}] message [{response}]')
        self.check_command_response(response, request)

    def get_state_request(self,
                          station_id: str,
                          station_sub_id: str,
                          object_type_name: str,
                          object_name: str,
                          object_state: str) -> str:
        if not (object_type_name in self.station.ungatherd_objects):
            raise BadSendMessageException(f'ERROR! Couldn`t find object [{object_type_name}] \
in model, for station [{self.station.name}]. See description file')
        object_type_id = self.station.ungatherd_objects[object_type_name]

        if object_type_id not in self.station.states:
            raise BadSendMessageException(f'ERROR! Couldn`t find states list for object [{object_type_id}] \
in model, for station [{self.station.name}]. See description file')

        if (object_state not in self.station.states[object_type_id]):
            raise BadSendMessageException(f'ERROR! Couldn`t find state [{object_state}] for object [{object_type_name}] \
in model, for station [{self.station.name}]. See description file')
        return f'{GET_PREFIX}:{station_id}:{station_sub_id}:{object_type_id}:{object_name}'

    def check_state_response(self,
                             response: str,
                             object_state: str) -> None:
        if response == RESPONSE_ERROR_ANSWER or response.endswith(RESPONSE_NO_ANSWER):
            raise BadResponsedMessageException(
                f'ERROR! Got bad response [{response}]')
        response_items = response.split(RESPONSE_SEP)
        object_type_id = int(response_items[2])
        layers: dict[LayerColor] = dict()
        for record in response_items[4:]:
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
                raise BadResponsedMessageException(
                    f'ERROR! Got wrong amount of object`s colors [{len(items)}]')

            for color, value in self.station.colors.items():
                if id_permanent_color in value:
                    permanent_color = color
                    break
            for color, value in self.station.colors.items():
                if id_blink_color in value:
                    blink_color = color
                    break
            if not permanent_color:
                raise BadResponsedMessageException(f'ERROR! Couldn`t find color [{id_permanent_color}] \
in model, for station [{self.station.name}]. See description file')
            if not permanent_color or not blink_color:
                raise BadResponsedMessageException(f'ERROR! Couldn`t find color [{id_permanent_color}] \
in model, for station [{self.station.name}]. See description file')

            layer_color = LayerColor(blink_color, permanent_color)
            layers[layer] = layer_color
        if object_type_id not in self.station.states:
            raise BadResponsedMessageException(f'ERROR! Couldn`t find object [{object_type_id}] \
in model, for station [{self.station.name}]. See description file')
        for lr in self.station.states[object_type_id][object_state]:
            if lr not in layers:
                raise BadResponsedMessageException(
                    f'ERROR! Couldn`t find layer [{lr}] for state [{object_state}]')
            if layers[lr] != (self.station.states[object_type_id][object_state][lr]):
                raise BadResponsedMessageException(f'ERROR! For object [{object_type_id}] in \
state [{object_state}] for layer [{lr}] expected state \
is [{self.station.states[object_type_id][object_state][lr].blink_color}: \
{self.station.states[object_type_id][object_state][lr].permanent_color}], \
got [{layers[lr].blink_color}: {layers[lr].permanent_color}]')

    def get_command_request(self,
                            station_id: str,
                            object_type_name: str,
                            object_name: str,
                            command_name: str,
                            command_type: str) -> str:

        command_type = command_type if command_type else '0'

        if not (object_type_name in self.station.ungatherd_objects):
            raise BadSendMessageException(f'ERROR! Couldn`t find object [{object_type_name}] \
in model, for station [{self.station.name}]. See description file')

        object_type_id = self.station.ungatherd_objects[object_type_name]

        if command_type not in '012':
            raise BadSendMessageException(
                f'ERROR! Wrong command type [{command_type}]')

        return f'{CMD_PREFIX}:{station_id}:{object_type_id}:{object_name}:{command_name}:{command_type}'

    def check_command_response(self, response: str, request: str) -> None:
        if response == RESPONSE_ERROR_ANSWER or response.endswith(RESPONSE_NO_ANSWER):
            raise BadResponsedMessageException(
                f'ERROR! Got bad response [{response}]')


class TesterTestRowHandler(AbstractTestRowHandler):

    def __init__(self, tester: Tester):
        self.tester = tester
        super().__init__()

    def handle(self, line: str, clients: Clients,  test_logger: AbstractTestLogger):
        marker, marker_sep, tail = line.partition(MARKER_SEP)
        if marker_sep and marker == MARKER_TESTER:
            try:
                params = [item.strip() for item in tail.split(PARAM_SEP)]
                params_length = len(params)
                if params_length == 4:
                    self.handle_state(params, clients, test_logger)
                elif params_length == 3:
                    self.handle_command(params, clients, test_logger)
                else:
                    message = f'ERROR! For Visualisation record [{line}] wrong params quantities [{params_length}]]'
                    raise BadSendMessageException(message)
            except (BadResponsedMessageException,
                    BadSendMessageException, TCPConnectionError) as ex:
                raise FailedTestException(ex.message)
        else:
            super().handle(line, clients, test_logger)

    def handle_state(self, params: list[str], clients: Clients, test_logger: AbstractTestLogger) -> None:
        TCP_id, table_id, impulse_name, impulse_state_raw = params
        impulse_state, elapsed_sep, time_elapsed = impulse_state_raw.partition(
            MARKER_ELAPSED_TIME)

        TCP_client = clients.get_by_name(TCP_id)
        request = self.get_state_request(table_id, impulse_name, impulse_state)

        if elapsed_sep:
            delta_time = DELTA_TIME
            if time_elapsed:
                try:
                    delta_time = int(time_elapsed)
                except (ValueError, TypeError):
                    raise BadSendMessageException(
                        f'ERROR! Couldn`t convert string [{time_elapsed}] in integer')
            finish_time = datetime.datetime.now() + datetime.timedelta(seconds=delta_time)

            while (datetime.datetime.now() < finish_time):
                try:
                    TCP_client.send(request, end='\n')
                    test_logger.write_test_log_report(
                        f'Send to client [{TCP_client.alias}] message [{request}]')
                    response = TCP_client.receive()
                    test_logger.write_test_log_report(
                        f'Receive from client [{TCP_client.alias}] message [{response}]')
                    self.check_state_response(
                        response, impulse_state)
                except (BadResponsedMessageException) as ex:
                    test_logger.write_test_log_report(ex.message)
                    time.sleep(1)
                else:
                    return None

        TCP_client.send(request, end='\n')
        test_logger.write_test_log_report(
            f'Send to client [{TCP_client.alias}] message [{request}]')
        response = TCP_client.receive()
        test_logger.write_test_log_report(
            f'Receive from client [{TCP_client.alias}] message [{response}]')
        self.check_state_response(response, impulse_state)

    def handle_command(self, params: list[str], clients: Clients, test_logger: AbstractTestLogger) -> None:
        TCP_id, table_id, command_name_raw = params
        command_name, _, command_type = command_name_raw.partition(
            COMMAND_SEP)

        TCP_client = clients.get_by_name(TCP_id)
        request = self.get_command_request(
            table_id, command_name, command_type)
        TCP_client.send(request, end='\n')
        test_logger.write_test_log_report(
            f'Send to client [{TCP_client.alias}] message [{request}]')
        response = TCP_client.receive()
        test_logger.write_test_log_report(
            f'Receive from client [{TCP_client.alias}] message [{response}]')
        self.check_command_response(response, request)

    def get_state_request(self, table_id: str, impulse_name: str, impulse_state: str) -> str:

        if (impulse_state not in self.tester.states):
            raise BadSendMessageException(f'ERROR! Couldn`t find state [{impulse_state}] \
in model, for tester [{self.tester.name}]. See description file')
        return f'{GET_PREFIX}:{table_id}:{impulse_name}'

    def check_state_response(self, response: str, impulse_state: str) -> None:
        if response == RESPONSE_ERROR_ANSWER or response.endswith(RESPONSE_NO_ANSWER):
            raise BadResponsedMessageException(
                f'ERROR! Got bad response [{response}]')
        table_id, impulse_name, response_impulse_state = response.split(
            RESPONSE_SEP)
        if not response_impulse_state.isdigit():
            raise BadResponsedMessageException(
                f'ERROR! Got bad state in response [{response}]')
        if self.tester.states[impulse_state] != int(response_impulse_state):
            raise BadResponsedMessageException(
                f'ERROR! For impulse [{impulse_name}] in \
table  [{table_id}] expected state is [{self.tester.states[impulse_state]}], \
got [{response_impulse_state}]')

    def get_command_request(self, table_id: str, command_name: str, command_type: str) -> str:
        if command_name.startswith('@'):
            if command_type not in '0123':
                raise BadSendMessageException(
                    f'ERROR! Wrong command type [{command_type}]')
        else:
            if command_type not in '01':
                raise BadSendMessageException(
                    f'ERROR! Wrong command type [{command_type}]')
        return f'{CMD_PREFIX}:{table_id}:{command_name}:{command_type}'

    def check_command_response(self, response: str, request: str) -> None:
        if response == RESPONSE_ERROR_ANSWER or response.endswith(RESPONSE_NO_ANSWER):
            raise BadResponsedMessageException(
                f'ERROR! Got bad response [{response}]')


class ConcreatTestRowHandler:
    def create(self, station_name: str) -> AbstractTestRowHandler:
        station = Station(station_name)
        tester = Tester(station_name)
        waiter_test_row_handler = WaiterTestRowHandler()
        vis_test_row_handler = VisTestRowHandler(station)
        tester_test_row_handler = TesterTestRowHandler(tester)
        waiter_test_row_handler.set_next(vis_test_row_handler)
        vis_test_row_handler.set_next(tester_test_row_handler)

        return waiter_test_row_handler
