import sys
from colorama import init
from app.classes.station_test.StationTest import StationTest
from config.config import STATION
from logger import get_logger

init(autoreset=True)
logger = get_logger(__name__)

if __name__ == '__main__':
    result = 1
    try:
        station = StationTest(STATION)
        if station.run():
            result = 0
    except Exception:
        logger.error('ERROR! Unhandled exception', exc_info=True)
    sys.exit(result)
