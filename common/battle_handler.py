# -*-coding:utf-8-*-
from tool.user_tool import UsersTool
from tool.room_tool import RoomTool
from tool.message_tool import gm_say, say
from common.response import Response
from common.utility import UserStatus


class BattleHandler(object):
    def __int__(self):
        pass

    @staticmethod
    def begin(room, clients):
        r_id = int(room['r_id'])
        room_clients = RoomTool.room_clients(clients, r_id)
        room_user = BattleHandler.begin_game(room_clients, r_id)
        for client in clients:
            if not client:
                continue
            user = UsersTool.update_user(client, status=UserStatus.playing)
        room, current_user, other_clients = room_user['room'], room_user['user'], room_user['other_clients']
        Response('rooms.begin', room).response(clients=clients)
        gm_say(u'游戏开始啦', room_clients)

    @staticmethod
    def start(data, client, clients):
        other_clients = filter(lambda u: id(u) != id(client),
                               RoomTool.room_clients(clients, UsersTool.current_user(client)['r_id']))
        data = {}
        Response('offline.start', data).response(clients=other_clients)


    @staticmethod
    def next_begin(client, clients):
        r_id = UsersTool.current_user(client)['r_id']
        room_clients = RoomTool.room_clients(clients, r_id)
        games = BattleHandler.begin_game(room_clients, r_id)
        room, current_user, over, other_clients = games['room'], games['user'], games['over'], games['other_clients']

        RoomTool.update_room(r_id, cantip=False)


    @staticmethod
    def judge(client, clients, topic, user, message):
        if BattleHandler.judge_song_result(topic, message):
            # self.next_begin()
            Response(header='rooms.willnext', data=10, msg=None).write_message_to(clients=clients)
            gm_say(u'%s 猜对啦, 开始下一首' % user['rolename'], clients)
        else:
            say(client, message, clients, 'rooms.message')

    @staticmethod
    def judge_song_result(topic, message):
        topic_title = topic['topic_title']

        if topic_title == message:
            return True
        return False

    @staticmethod
    def current_topic(r_id):

        room = RoomTool.room_by(r_id)

        if room['status'] != RoomStatus.playing:
            return None

        users = UsersTool.room_users(r_id)

        for user in users:
            if user:
                if user.get('status', None) == Status.action:
                    return user['topic']

        return None
