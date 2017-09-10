#!/bin/env python
# -*-coding:utf-8-*-


from common.game_handler import GameMessageHanlder
import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
import json

from common.redis_ctl import redis_obj


class GameHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        print "connect"
        self.application.handler.clients[str(id(self))] = self

    def on_close(self):
        self.application.handler.quit(self)

    def on_message(self, message):
        packet = json.loads(message)
        self.application.handler.handle(self, packet)


class GameApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', GameHandler),
        ]
        self.handler = GameMessageHanlder()
        super(GameApplication, self).__init__(handlers)


def main():
    http = tornado.httpserver.HTTPServer(GameApplication())
    http.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
   main()


