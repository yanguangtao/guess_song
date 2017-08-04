#!/bin/env python
# -*-coding:utf-8-*- 

import re
import datetime
import hashlib
import time
import traceback
import requests
from decimal import Decimal
from flask import jsonify
from IPy import IP
from sqlalchemy.ext.declarative import DeclarativeMeta

from conf import settings
from common.my_log import logger
from sqlalchemy_ctl import Base
from sqlalchemy_ctl import DBSession
from sqlalchemy_ctl import engine

def create_table(table_name=""):
    if table_name == "":
        Base.metadata.create_all(engine)
    else:
        Base.metadata.tables[table_name].create(bind=engine, checkfirst=True)


def drop_table(table_name=""):
    if table_name == "":
        Base.metadata.drop_all(engine)
    else:
        Base.metadata.tables[table_name].drop(bind=engine, checkfirst=True)


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


def valid_ip(ip_str):
    """
    判断IP字符串是否有效IP
    :param ip_str: 字符串
    :return: 有效则返回True, 无效返回False
    """
    pattern = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if re.match(pattern, ip_str):
        return True
    else:
        return False


def check_ip(input_ip):
    """ 校验IP """
    if not input_ip:
        return False
    len_ip = input_ip.split('.')
    if len(len_ip) != 4:
        return False
    try:
        result = IP(input_ip)
        return result
    except Exception as e:
        logger.error(u'输入的IP [ %s ] 不正确。错误信息：%s' % (input_ip, e))
        return False


def check_mask(input_mask):
    """校验掩码 """
    result_mask = check_ip(input_mask)
    if not result_mask:
        return False
    # 将掩码转换为二进制格式，合法掩码：前面部分全是1，后面部分全是0
    mask_bin = result_mask.strBin()
    if not mask_bin.startswith('1'):
        logger.error(u'输入的掩码 [ %s ] 不合法' % input_mask)
        return False
    # 子网号长度
    subnet_number = 0
    for i in mask_bin:
        # 统计掩码中的子网号
        if i == '1':
            subnet_number += 1
        else:
            break
    # 获取子网中的主机号
    host_number = '0' * (32-subnet_number)
    # 输入的主机号
    input_host_number = mask_bin[subnet_number:]
    if host_number != input_host_number:
        logger.error(u'输入的掩码 [ %s ] 不正确' % input_mask)
        return False
    return input_mask


def check_network_segment(input_ip, input_mask):
    """ 校验网段：网络号+掩码 """
    try:
        result_ip = check_ip(input_ip)
        result_mask = check_mask(input_mask)
        # IP 掩码校验都正确
        if result_ip and result_mask:
            result = IP('%s/%s' % (input_ip, input_mask))
            return result
        return False
    except Exception as e:
        logger.error(u'输入的网段 [ %s/%s ] 不正确。错误信息：%s' % (input_ip, input_mask, e))
        return False


def get_session_user_id(sessionid):
    """通过sessionid获取登录用户id"""
    params = {"sessionid": sessionid}
    response = requests.get(settings.IPORTAL_SESSIONID['url'], params=params).json()
    if response.get("ret", 1) == 0:
        user_info = response.get("data", {}).get("user_info", {})
        user_id = int(user_info.get("user_id", -1))
    else:
        user_id = '-1'
    return user_id


def get_user_from_session(sessionid):
    """通过sessionid获取登录用户信息"""
    params = {"sessionid": sessionid}
    try:
        response = requests.get(settings.IPORTAL_SESSIONID['url'], params=params, timeout=5).json()
    except Exception as e:
        logger.error(u"查询失败：%s, %s" % (settings.IPORTAL_SESSIONID['url'], e))
        return {}
    if response.get("ret", 1) == 0:
        user_info = response.get("data", {}).get("user_info", {})
    else:
        user_info = {}
    return user_info


def get_user_list():
    """获取用户列表"""
    user_list = []
    try:
        response = requests.get(settings.USER_CENTER_API['user_url'], timeout=5).json()
        if response.get("ret", 1) == 0:
            user_list = response.get("data", [])
        else:
            raise Exception
    except Exception as e:
        logger.error(u"无法获取iportal用户列表:%s" % str(e))
    return user_list


def get_department_list():
    """获取用户列表"""
    department_list = []
    try:
        response = requests.get(settings.USER_CENTER_API['department_url'], timeout=5).json()
        if response.get("ret", 1) == 0:
            department_list = response.get("data", [])
        else:
            raise Exception
    except Exception as e:
        logger.error(u"无法获取iportal用户列表:%s" % str(e))
    return department_list


def send_email(subject, content, to_addrs):
    """
    发送邮件
    :param subject: 邮件标题
    :param content: 邮件正文
    :return:
    """
    try:
        email_info = {'to_addrs': to_addrs,
                      'subject': subject,
                      'content': content,
                      'content_subtype': 'html'}
        requests.post(settings.EMAIL_API, email_info)
        return True
    except Exception as e:
        logger.error("发送邮件失败, ERROR:%s" % str(e))
        return False


def is_local_ip(ip):
    if re.match('10\.|172\.1[6-9]|172\.2[0-9]|172\.3[0-1]|192\.168\.', ip):
        return True
    return False

