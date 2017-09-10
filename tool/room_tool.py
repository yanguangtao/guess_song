#!/bin/env python
#!/bin/env python
# -*-coding:utf-8-*-
from random import Random
from common import error_msg
from common.redis_ctl import redis_obj
from common.utility import RoomStatus, GameType, BattleType, UserStatus, get_room_key, get_w_key
from tool.user_tool import UsersTool


class RoomTool(object):

    @staticmethod
    def random_str(length=8):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(length):
            str += chars[random.randint(0, length)]
        return str

    @staticmethod
    def init_rooms(user_id, client, battle_type=BattleType.freestyle, game_type=GameType.offline):
        room_id = user_id + "-" + RoomTool.random_str(8)
        blue = []
        w_id = str(id(client))
        if game_type == GameType.offline:
            blue = [user_id]
        room = {
            'room_id': room_id,
            'users': [],
            'w_id': w_id,
            'status': RoomStatus.waiting,
            'game_type': game_type,
            'battle_type': battle_type,
            'room_manege': 0,
            'blue': blue,
            'red': []
        }
        redis_obj.db.hmset(room_id, room)
        return room

    @staticmethod
    def update_room(room_id, **kwargs):
        """
        users,status,blue,red,room_manage
        :param room_id:
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            redis_obj.db.hset(room_id, str(k), k)
        return RoomTool.room_by(room_id)

    @staticmethod
    def room_clients(clients, room_id):
        room_key = get_room_key(room_id)
        users = redis_obj.db.hget(room_key, 'users')
        return map(lambda u: u is not None and clients[u['w_id']], users)

    @staticmethod
    def room_by(room_id):
        room = redis_obj.db.hgetall(get_room_key(room_id))
        room['users'] = room['users']
        return room

    @staticmethod
    def check_room_status(room_id):
        room = redis_obj.db.hgetall(room_id)
        if not room:
            return error_msg.ROOM_NOT_EXIST
        if room['status'] == RoomStatus.playing:
            return error_msg.ROOM_IS_START
        if room['battle_type'] == BattleType.two_bettal and len(room['users']) == 2:
            return error_msg.ROOM_IS_FULL
        elif room['battle_type'] == BattleType.freestyle and len(room['users']) == 6:
            return error_msg.ROOM_IS_FULL
        return error_msg.SUCCESS

    @staticmethod
    def room_users(room_id):
        return redis_obj.db.hget(room_id, 'users')

    @staticmethod
    def enter_room(client, room_id):
        code, msg = RoomTool.check_room_status(room_id)
        if code != 0:
            return code, msg
        users = RoomTool.room_users(room_id)
        UsersTool.update_user(client, r_id=room_id, status=UserStatus.waiting)
        for i in range(0, len(users)):
            if not users[i]:
                user = UsersTool.update_user(client)
                users[i] = user
                break
        room = RoomTool.update_room(room_id, users=users)
        return room

    @staticmethod
    def leave_room(client, room_id=None):
        if room_id is None:
            user = UsersTool.current_user(client)
            room_id = int(user.get('r_id', -1))
            if room_id == -1:
                return None
        users = RoomTool.room_users(room_id)
        users.remove(redis_obj.db.get(get_w_key(client)))
        RoomTool.update_room(room_id, users=users)
        if not users:
            RoomTool.delete_room(room_id)
        UsersTool.update_user(client, r_id=-1, status=UserStatus.free)
        return RoomTool.room_by(room_id)

    @staticmethod
    def delete_room(room_id):
        room_key = get_room_key(room_id)
        redis_obj.db.delete(room_key)

    @staticmethod
    def game_over(clients, room_id):
        users = UsersTool.room_users(get_room_key(room_id))
        for client in clients:
            if client:
                UsersTool.update_user(client, status=UserStatus.free)
        return RoomTool.delete_room(room_id)

    @staticmethod
    def change_position(client, room_id, p_id):
        users = RoomTool.room_users(room_id)
        user = UsersTool.update_user(client, p_id=p_id)
        room = RoomTool.update_room(room_id, users=users)
        return room
