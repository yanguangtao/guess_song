#!/bin/env python
# -*- coding:utf8 -*-



class LocalConfig(object):
    DEBUG = True
    CREATE_TABLE = True
    # 生产新数据库
    # MYSQL_HOST = "192.168.13.39"
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "yan718844"
    MYSQL_DB = "guess_song"

    # 本地运维平台redis信息
    REDIS_HOST ="119.23.210.27"
    REDIS_PORT = 6379
    REDIS_DB = 1
    REDIS_PWD = ""
    # 3小时后自动重连mysql
    MYSQL_CONNECT_TIMEOUT = 3 * 60 * 60

    # token
    # 7天有效期
    TOKEN_TIMEOUT = 7 * 24 * 60 * 60
