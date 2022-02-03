# -*- coding: utf-8 -*-
# class BadPayloadDataException(Exception):
#     def __init__(self, data_len: int) -> None:
#         self.message = f'Wrong data length = {data_len}'


class DublicateKeyException(Exception):
    pass


class NotFoundKeyException(Exception):
    pass


class UnhandledRowException(Exception):
    pass
