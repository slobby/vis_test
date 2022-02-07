import socket
from constants import CODE_PAGE, TIMEOUT
from logger import get_logger

from config.config import SERVER_HOST, SERVER_PORT

logger = get_logger(__name__)


def send_and_recieve(message, ip=SERVER_HOST, port=SERVER_PORT) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT)
        sock.connect((ip, port))
        logger.info(f'Connect to server {ip}:{port}')
        sock.sendall(bytes(message, CODE_PAGE))
        logger.info(f'Send to server [{message}]')
        response = str(sock.recv(1024), CODE_PAGE).strip(' \r\n')
        logger.info(f'Recieve from server [{response}]')
        return response
