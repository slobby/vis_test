import os
import sys
from colorama import init
import click
from importlib.util import module_from_spec, spec_from_file_location
from app.classes.TCPClient import Clients
from app.classes.StationTest import StationTest
from app.classes.TestRowHandler import ConcreatTestRowHandler
from app.exceptions import TCPConnectionError

from constants import CONFIG, VIS_TEST_VERBOSE, VIS_TEST_VERBOSE_YES
from logger import get_logger

init(autoreset=True)
logger = get_logger(__name__)


@click.command()
@click.option('-c', '--config', 'config_file', default='config',
              help='Config file name.')
@click.option('-s', '--success', 'success', multiple=True,
              help='Test files executed after every successful test. \
Can be multiple.')
@ click.option('-t', '--test', 'tests', multiple=True,
               help='Test file/folder name in station folder. Can be multiple.')
@ click.option('-f', '--fixture', 'fixtures', multiple=True,
               help='Test files executed after every failed test. \
Can be multiple.')
@ click.option('-r', '--repeat', 'repeat', default=1,
               help='Set repeat tests (if they are succsseful).')
@ click.option('-v', '--verbose', is_flag=True,
               help='Show more info.')
def main(config_file, tests, success, fixtures, repeat, verbose):
    success_all_tests = False
    clients = None
    if verbose:
        os.environ[VIS_TEST_VERBOSE] = VIS_TEST_VERBOSE_YES

    try:
        config = get_config_module(config_file)
        test_row_handler = ConcreatTestRowHandler().create(config.STATION)
        clients = Clients(config)
        station_test = StationTest(
            config.STATION, clients, test_row_handler, tests, success, fixtures)
        for i in range(1, repeat+1):
            print(
                f'\n===================== test cicle №-{i} =====================\n')
            if not station_test.run():
                break
        else:
            success_all_tests = True
    except TCPConnectionError as ex:
        logger.error(ex.message)
    except Exception:
        logger.error('ERROR! Unhandled exception', exc_info=True)
    finally:
        if clients:
            for id_client in clients:
                clients[id_client].close()

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


if __name__ == '__main__':
    main()
