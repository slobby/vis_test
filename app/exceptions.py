# -*- coding: utf-8 -*-
# class BadPayloadDataException(Exception):
#     def __init__(self, data_len: int) -> None:
#         self.message = f'Wrong data length = {data_len}'

class VisTestException(Exception):
    pass


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
    pass


class BadResponsedMessageException(VisTestException):
    pass
