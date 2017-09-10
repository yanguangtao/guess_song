#!/bin/env python
# -*-coding:utf-8-*-


from common.redis_ctl import redis_obj
from common.utility import get_user_key, get_w_key, UserStatus, to_dict_obj
from user.user_controller import user_controller
from user.user_model import UserModel


class UsersTool(object):
    @staticmethod
    def login(client, data):
        user = user_controller.login(data)

        if user:
            user = to_dict_obj(user)
            print user
            u_id, w_id = user['id'], str(id(client))
            user_key = get_user_key(u_id)
            # record online user
            redis_user = redis_obj.db.hgetall(user_key)
            if not redis_user:
                redis_user = {
                    'u_id': u_id,  # user id
                    'w_id': w_id,  # websocket id
                    'r_id': -1,  # room
                    'p_id': 0, #0blue 1red
                    'status': UserStatus.free,
                }
            else:
                redis_user['w_id'] = w_id
            redis_obj.db.hmset(user_key, redis_user)
            # associated webSocket and user
            redis_obj.db.set(get_w_key(client), u_id)
            user["p_id"] = redis_user["p_id"]
            user["r_id"] = redis_user["r_id"]
            user['status'] = redis_user["status"]
        return user

    @staticmethod
    def is_login(client):
        result = True if redis_obj.db.get(get_w_key(client)) else False
        return result

    @staticmethod
    def quit(client, clients):
        from tool.room_tool import RoomTool
        room = RoomTool.leave_room(client)
        user = UsersTool.current_user(client)
        w_key = get_w_key(client)
        u_id = redis_obj.db.get(w_key)
        u_key = get_user_key(u_id)
        if w_key is None or u_key is None:
            return None
        redis_obj.db.delete(w_key)
        redis_obj.delete(u_key)
        del clients[str(id(client))]
        return user, room


    @staticmethod
    def update_user(client, r_id=None, status=None, p_id=None):
        u_id = redis_obj.db.get(get_w_key(client))
        u_key = get_user_key(u_id)
        if r_id is not None:
            redis_obj.db.hset(u_key, 'r_id', r_id)
        if status is not None:
            redis_obj.db.hset(u_key, 'status', status)
        if p_id is not None:
            redis_obj.db.hset(u_key, 'p_id', p_id)
        return UsersTool.current_user(client)

    @staticmethod
    def current_user(client):
        u_id = redis_obj.db.get(get_w_key(client))
       # user_info = db.query(UserModel).filter_by(id=u_id).first()
        user_info = None
        return user_info.to_dict_obj(user_info)

    @staticmethod
    def current_users(client, clients):
        users = list()
        for other in clients:
            if other == client:
                continue
            user = UsersTool.current_user(other)
            if user:
                users.append(user)
        return users
