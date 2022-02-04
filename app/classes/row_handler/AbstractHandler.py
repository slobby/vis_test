from abc import ABC, abstractmethod


class AbstractRowHandler(ABC):

    next_handler: 'AbstractRowHandler' = None

    @abstractmethod
    def handle(self, row: list[str], station) -> None:
        pass

    def setNext(self, handler: 'AbstractRowHandler') -> None:
        self.next_handler = handler
