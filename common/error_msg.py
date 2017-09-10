#!/bin/env python
# -*- coding:utf8 -*-

SUCCESS = 0, ""
SERVER_ERROR = -1, u"服务器异常"
ROOM_NOT_EXIST = 1, u"房间不存在"
ROOM_IS_FULL = 2, u"房间已满人"
ROOM_IS_START = 3, u"游戏已经开始"
NEW_ACCOUNT_ERROR = 4, u"用户名重复"
EMAIL_NAME_ERROR = 5, u"用户名非法"
PWD_ERROR = 6, u"密码错误"
OLD_PWD_ERROR = 7, u"旧密码错误"
SESSION_ERROR = 8, u"登录过期"
PARAMS_ERROR = 9, u"参数错误"

