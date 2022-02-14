import os
import sys
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
              help='Test file name in station folder. Can be multiple.')
@click.option('-f', '--fixture', 'fixtures', multiple=True,
              help='Test file execuded before every test file.')
@click.option('-v', '--verbose', is_flag=True,
              help='Show more info.')
def main(config_file, tests, fixtures, verbose):
    if verbose:
        os.environ[VIS_TEST_VERBOSE] = VIS_TEST_VERBOSE_YES

    try:
        config = get_config_module(config_file)
        station = Station(config.STATION)
        client = TCPClient(config.SERVER_HOST, config.SERVER_PORT)
        station_test = StationTest(station, client, tests, fixtures)
        if station_test.run():
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
