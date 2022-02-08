from colorama import init
from app.classes.station_test.StationTest import StationTest
from config.config import STATION
from logger import get_logger

init(autoreset=True)
logger = get_logger(__name__)

if __name__ == '__main__':
    try:
        station = StationTest(STATION)
        station.run()
    except Exception:
        logger.error('ERROR! Unhandled exception', exc_info=True)
