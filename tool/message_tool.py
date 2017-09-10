#!/bin/env python
# -*-coding:utf-8-*-
from common.response import Response
from tool.room_tool import RoomTool
from tool.user_tool import UsersTool


def say(client, message, clients, header):
    user = UsersTool.current_user(client)
    user['message'] = message
    Response(header=header, data=user).response(clients=clients)


def say_hall(self, data):
    message = data.get('message', None)
    say(self.client, message, self.clients, 'hall.message')


def say_room(self, data):
    message, r_id = data.get('message', None), data.get('room_id', None)
    clients = RoomTool.room_clients(self.clients, r_id)
    user = UsersTool.current_user(self.client)
    say(self.client, message, clients, 'rooms.message')


def gm_say(message, clients=None, client=None):
    response = Response(header='rooms.message', data={'rolename': 'GM', 'message': message})
    if client is not None:
        response.response(client)
    else:
        response.response(clients=clients)