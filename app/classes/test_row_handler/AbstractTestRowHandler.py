from abc import ABC, abstractmethod


class AbstractTestRowHandler(ABC):

    next_handler: 'AbstractTestRowHandler' = None

    def __init__(self, test_task):
        self.test_task = test_task

    @abstractmethod
    def handle(self, row: list[str]) -> None:
        pass

    def set_next(self, handler: 'AbstractTestRowHandler') -> None:
        self.next_handler = handler
