import os
import click
from constants import VIS_TEST_VERBOSE, VIS_TEST_VERBOSE_YES


@click.command()
@click.option('-c', '--config', 'config_file', default='config',
              help='Config file name.')
@click.option('-t', '--test', 'tests', multiple=True,
              help='Test file name in station folder. Can be multiple.')
@click.option('-f', '--fixture', 'fixtures', multiple=True,
              help='Test file execuded before every test file.')
@click.option('-v', '--verbose', is_flag=True,
              help='Show more info.')
def menue(config_file, tests, fixtures, verbose):
    if verbose:
        os.environ[VIS_TEST_VERBOSE] = VIS_TEST_VERBOSE_YES
    return config_file, tests, fixtures
