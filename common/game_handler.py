# coding: utf-8

import time
import threading


from common.my_log import logger
from common.redis_ctl import redis_obj

from tool.message_tool import gm_say, say
from tool.room_tool import RoomTool
from tool.user_tool import UsersTool

from common.response import Response
from common.utility import check_session, GameType, BattleType, get_w_key



class GameMessageHanlder:

    def __init__(self):
        self.clients = dict()
        self.client = None

        from common.battle_handler import BattleHandler
        self.battle_handler = BattleHandler()

    def invalid(self):
        pass

    def handle(self, client, packet):
        self.client = client
        try:
            # headers = str.split()packet.get('header', "")
            # create_obj = compile('obj()', 'create_obj.py', 'eval')
            # a = eval(create_obj)
            # method = getattr(self, packet['header'])
            method = getattr(self, packet['header'])
            (method(packet['data']) if 'data' in packet else method()) if method else self.invalid()
        except AttributeError as e:
            logger.error(e)

    # handle common operation
    def main_handle(self, data):
        session = data.get("session", None)
        if not data.get("session", None) or not check_session(session):
            data = {"msg": "", "code": 1, "data": {}}
            Response('main', data).response(self.client)
        else:
            Response('main', data).Response(self.client)

    # 用户
    def login(self, data):

        data = UsersTool.login(client=self.client, data=data)
        Response('user.login', data=data).response(self.client)

    def quit(self, client):
        if not UsersTool.is_login(client):
            return
        user, room = UsersTool.quit(client, self.clients)
        if user:
            Response('user.leave', data=user).response(clients=self.clients)
        if room:
            Response('room.info', data=room).response(clients=self.clients)

    # 房间
    def create_room(self, data=None):
        user_id = redis_obj.db.get(get_w_key(self.client))
        room = RoomTool.init_room(user_id, self.client, BattleType.freestyle, GameType.offline)
        Response("room.create", room).response(self.client)

    def enter_room(self, data):
        room_id, p_id = data.get('room_id', None), data.get('p_id', None)
        room = RoomTool.enter_room(self.client, room_id, p_id)
        room_id = room["r_id"]
        Response('room.info', data=room).response(clients=self.clients)
        Response('room.enter', data=room_id).response(self.client)
        gm_say('欢迎来到猜歌王', client=self.client)

    def leave_room(self, data):
        user_id = redis_obj.db.get(get_w_key(self.client))
        room = RoomTool.init_room(user_id, self.client, BattleType.freestyle, GameType.offline)
        Response("room.create", room).response(self.client)
        room_id, p_id = data.get('room_id', None), data.get('p_id', None)
        room = RoomTool.leave_room(self.client, room_id, p_id)
        Response('room.leave', data={}).response(self.client)
        Response('room.info', data=room).response(clients=self.clients)

    def change_position(self, data):
        room_id, p_id = data.get('room_id', None), data.get('p_id', 0)
        try:
            p_id = int(p_id)
            room = RoomTool.change_position(self.client, room_id, p_id)
            if room is not None:
                Response('room.info', room).response(clients=self.clients)
        except TypeError as e:
            logger.error(e)
    
    # 游戏结束后再来一局
    def next_begin(self, data):
        room_id = data.get('room_id', None)
        game_type = RoomTool.room_by(room_id)['game_type']
        if game_type == GameType.offline:
            self.battle_handler.next_begin(self.client, self.clients)

    # handle game
    def battle_start(self, data):
        self.battle_handler.start(data, self.client, self.clients)
        
    def leave(self, data):
        room_id, p_id = data.get('room_id', None), data.get('p_id', None)
        room = RoomTool.leave_room(self.client, room_id, p_id)
        Response('room.leave', data={}).response(self.client)
        Response('room.info', data=room).response(clients=self.clients)


