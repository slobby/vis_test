import os
import sys
from colorama import init
import click
from importlib.util import module_from_spec, spec_from_file_location

from constants import CONFIG, VIS_TEST_VERBOSE, VIS_TEST_VERBOSE_YES

init(autoreset=True)


@click.command()
@click.option('-c', '--config', 'config_file', default='config',
              help='Config file name.')
@click.option('-t', '--test', 'tests', multiple=True,
              help='Test files name in station folder. Can be multiple.')
@click.option('-f', '--fixture', 'fixtures', multiple=True,
              help='Test files executed after every failed test. \
Can be multiple.')
@click.option('-r', '--repeat', 'repeat', default=1,
              help='Set repeat tests (if they are succssesful).')
@click.option('-v', '--verbose', is_flag=True,
              help='Show more info.')
def main(config_file, tests, fixtures, repeat, verbose):
    if verbose:
        os.environ[VIS_TEST_VERBOSE] = VIS_TEST_VERBOSE_YES
    from app.classes.TCPClient import TCPClient
    from app.classes.station.Station import Station
    from app.classes.station_test.StationTest import StationTest
    from app.exceptions import TCPConnectionError

    from logger import get_logger
    logger = get_logger(__name__)
    try:
        config = get_config_module(config_file)
        station = Station(config.STATION)
        client = TCPClient(config.SERVER_HOST, config.SERVER_PORT)
        station_test = StationTest(station, client, tests, fixtures)
        while repeat > 0:
            if not station_test.run():
                break
            repeat -= 1
            if repeat <= 0:
                sys.exit(0)
    except TCPConnectionError as ex:
        logger.error(ex.message)
    except Exception:
        logger.error('ERROR! Unhandled exception', exc_info=True)
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
