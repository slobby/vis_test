# -*- coding: utf-8 -*-
# class BadPayloadDataException(Exception):
#     def __init__(self, data_len: int) -> None:
#         self.message = f'Wrong data length = {data_len}'

class TCPConnectionError(Exception):
    message: str = None

    def __init__(self, message=None):
        self.message = message


class VisTestException(Exception):
    message: str = None

    def __init__(self, message=None):
        self.message = message


class DublicateKeyException(VisTestException):
    pass


class NotFoundKeyException(VisTestException):
    pass


class UnhandledRowException(VisTestException):
    pass


class DublicateLayerException(VisTestException):
    pass


class FailedTestException(VisTestException):
    pass


class UnhandledTestRowException(VisTestException):
    pass


class BadSendMessageException(VisTestException):
    def __init__(self, message=None):
        super().__init__(message)


class BadResponsedMessageException(VisTestException):
    def __init__(self, message=None):
        super().__init__(message)
