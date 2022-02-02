from abc import ABC, abstractmethod

from Station import Station


class AbstractRowHandler(ABC):

    next: 'AbstractRowHandler'

    @abstractmethod
    def handle(self, row: list[str], station: Station) -> None:
        pass

    def setNext(self, h: 'AbstractRowHandler') -> None:
        self.next = h
