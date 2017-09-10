#!/bin/env python
# -*-coding:utf-8-*- 

import re
import datetime
import hashlib
import time
import traceback
import requests
from decimal import Decimal
from sqlalchemy.ext.declarative import DeclarativeMeta

from conf import settings
from common.my_log import logger
from sqlalchemy_ctl import Base
from sqlalchemy_ctl import DBSession
from sqlalchemy_ctl import engine


def create_table(tablename=""):
    if tablename == "":
        Base.metadata.create_all(engine)
    else:
        Base.metadata.tables[tablename].create(bind=engine, checkfirst=True)


def drop_table(tablename=""):
    if tablename == "":
        Base.metadata.drop_all(engine)
    else:
        Base.metadata.tables[tablename].drop(bind=engine, checkfirst=True)


def to_dict_obj(
        orm_obj,
        need_fields=None,
        without_fields=None,
        datetime_format="%Y-%m-%d"):
    if isinstance(orm_obj, list):
        return [to_dict_obj(i, need_fields, without_fields, datetime_format) for i in orm_obj]
    elif isinstance(orm_obj.__class__, DeclarativeMeta):
        attr_dict = dict()
        for attr in [x for x in dir(orm_obj) if not x.startswith('_') and x != 'metadata']:
            data = getattr(orm_obj, attr)
            if need_fields and attr not in need_fields:
                continue
            if without_fields and attr in without_fields:
                continue
            if isinstance(data, datetime.datetime):
                attr_dict[attr] = data.strftime(datetime_format)
                if attr_dict[attr] == "1970-01-01":
                    attr_dict[attr] = ""
            elif isinstance(data, datetime.date):
                attr_dict[attr] = data.strftime("%Y-%m-%d")
            elif isinstance(data, datetime.timedelta):
                attr_dict[attr] = ((datetime.datetime.min + data).time().
                                   strftime("%Y-%m-%d %H:%M:%S"))
            elif isinstance(data, Decimal):
                attr_dict[attr] = float(data)
            else:
                attr_dict[attr] = data
        return attr_dict
    else:
        return orm_obj


def enum(**enums):
    return type('Enum', (), enums)

RoomStatus = enum(
    full='full',
    ready='ready',
    playing='playing',
    waiting='waiting'
)
GameType = enum(
    online='online',
    offline='offline'
)
BattleType = enum(
    freestyle='freestyle',
    one_battle='1v1',
    two_battle='2v2'
)
UserStatus = enum(
    free='free',
    waiting='waiting',
    ready='ready',
    playing='playing',
    action='action'
)


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        instances[cls].__dict__.update(kwargs)
        return instances[cls]
    return _singleton


def check_session(func):
    def wrapper(self, *args, **kwargs):
        if not True:
            return
        func(self, *args, **kwargs)
    return wrapper()

def get_w_key(client):
    return 'w_id:%s' % str(id(client))


def get_user_key(u_id):
    return 'user:%s' % str(u_id)


def get_room_key(room_id):
    return 'room:%s' % str(room_id)

