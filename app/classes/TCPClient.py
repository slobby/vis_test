import socket
import time
from types import ModuleType
from app.exceptions import TCPConnectionError
from constants import CODE_PAGE, CON_ATTEMPTS, TIMEOUT
from logger import get_logger

__all__ = ['TCPClient', 'Clients']

logger = get_logger(__name__)


class TCPClient():

    _sock: socket.socket = None

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._con_attempts = CON_ATTEMPTS
        self._create()
        self._connect()

    def _create(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(TIMEOUT)

    def _connect(self):
        try:
            self._sock.connect((self._host, self._port))
        except Exception:
            self._reconnect()
        logger.info(f'Connect to server {self._host}:{self._port}')

    def _reconnect(self):
        try:
            if (self._con_attempts > 0):
                if (not self._is_connected()):
                    time.sleep(0.5)
                    if self._sock:
                        self.close()
                    self._create()
                    self._sock.connect((self._host, self._port))
            else:
                raise TCPConnectionError()
        except TCPConnectionError:
            raise TCPConnectionError(f'ERROR! Couldn`t establish a connection \
on {self._host}, {self._port} in {CON_ATTEMPTS} attempts')
        except (ConnectionRefusedError, socket.timeout):
            logger.warning(
                f'Couldn`t establish a connection \
on {self._host}, {self._port} during {self._con_attempts} attempt')
            if self._con_attempts > 0:
                self._con_attempts -= 1
                self._reconnect()
        else:
            self._con_attempts = CON_ATTEMPTS

    def _is_connected(self):
        try:
            if self._sock:
                ping_bytes = b'GET'
                self._sock.sendall(ping_bytes)
                self._sock.recv(1024)
                return True
            else:
                return False
        except Exception:
            return False

    def close(self):
        if self._sock:
            self._sock.close()

    def send(self, message: str):
        try:
            if self._sock:
                self._sock.sendall(bytes(message, CODE_PAGE))
                logger.info(
                    f'Send to [{self._host}, {self._port}] \
message [{message}]')
        except Exception:
            self._reconnect()
            self.send(message)

    def receive(self) -> str:
        try:
            if self._sock:
                response = str(self._sock.recv(1024), CODE_PAGE).strip(' \r\n')
                logger.info(
                    f'Recieve from [{self._host}, {self._port}] \
message [{response}]')
            return response
        except Exception:
            raise TCPConnectionError(
                f'ERROR! Couldn`t recieve message \
from {self._host}, {self._port}')


class Clients():
    _clients: dict[TCPClient]
    _default_client_name: str

    def __init__(self, config: ModuleType):
        if config.CLIENTS:
            self._clients = {key: TCPClient(*value)
                             for key, value in config.CLIENTS.items()}
        else:
            self._clients = {config.CLIENT_ID: TCPClient(
                config.CLIENT_HOST, config.CLIENT_PORT)}
        self._default_client_name = config.CLIENT_ID

    def get_by_name(self, name: str = None) -> TCPClient:
        if name is None:
            return self._clients[self._default_client_name]
        if name in self._clients:
            return self._clients[name]
        message = f'ERROR! Couldn`t find object [{alias_object}] \
in station model [{self.test_task.station.name}]'
        self.test_task.write_test_log_report(message)
        raise BadSendMessageException(message)
