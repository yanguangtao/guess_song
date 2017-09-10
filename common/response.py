#!/bin/env python
# -*-coding:utf-8-*-
from common.utility import singleton
from tool.user_tool import UsersTool


@singleton
class Response(object):

    def __init__(self, header, data, ret=0, msg=""):
        self.header = header
        self.data = data
        self._msg = msg
        self._ret = ret

    def response(self, client=None, clients=None):
        message = {"data": self.data, "msg": self._msg, "ret": self._ret, "header": self.header}
        if client:
            client.write_message(message)
        elif clients:
            if isinstance(clients, dict):
                for c in clients.values():
                    if UsersTool.is_login(c):
                        c.write_message(message)
            elif isinstance(clients, list):
                for c in clients:
                    if UsersTool.is_login(c):
                        c.write_message(message)