import os
import sys
from types import ModuleType
from colorama import init
import click
from importlib.util import module_from_spec, spec_from_file_location
from app.classes.TCPClient import TCPClient
from app.classes.station.Station import Station
from app.classes.station_test.StationTest import StationTest
from app.exceptions import TCPConnectionError

from constants import CONFIG, VIS_TEST_VERBOSE, VIS_TEST_VERBOSE_YES
from logger import get_logger

init(autoreset=True)
logger = get_logger(__name__)


@click.command()
@click.option('-c', '--config', 'config_file', default='config',
              help='Config file name.')
@click.option('-t', '--test', 'tests', multiple=True,
              help='Test file/folder name in station folder. Can be multiple.')
@click.option('-f', '--fixture', 'fixtures', multiple=True,
              help='Test files executed after every failed test. \
Can be multiple.')
@click.option('-r', '--repeat', 'repeat', default=1,
              help='Set repeat tests (if they are succsseful).')
@click.option('-v', '--verbose', is_flag=True,
              help='Show more info.')
def main(config_file, tests, fixtures, repeat, verbose):
    success_all_tests = False
    client = None
    if verbose:
        os.environ[VIS_TEST_VERBOSE] = VIS_TEST_VERBOSE_YES

    try:
        config = get_config_module(config_file)
        station = Station(config.STATION)
        clients = get_TCP_clients(config)
        station_test = StationTest(station, clients, tests, fixtures)
        while repeat > 0:
            if not station_test.run():
                break
            repeat -= 1
        else:
            success_all_tests = True
    except TCPConnectionError as ex:
        logger.error(ex.message)
    except Exception:
        logger.error('ERROR! Unhandled exception', exc_info=True)
    finally:
        if client:
            client.close()

    if success_all_tests:
        sys.exit(0)
    else:
        sys.exit(1)


def get_config_module(config_file: str):
    config_path = os.path.join(CONFIG,
                               config_file + '.py')
    spec = spec_from_file_location(CONFIG, config_path)
    config = module_from_spec(spec)
    spec.loader.exec_module(config)
    return config


def get_TCP_clients(config: ModuleType) -> dict[TCPClient]:
    if config.CLIENTS:
        clients = {key: TCPClient(*value)
                   for key, value in config.CLIENTS.items()}
    else:
        clients = {config.CLIENT_ID: TCPClient(
            config.CLIENT_HOST, config.CLIENT_PORT)}
    return clients


if __name__ == '__main__':
    main()
