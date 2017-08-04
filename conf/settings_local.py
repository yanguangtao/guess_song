#!/bin/env python
# -*- coding:utf8 -*-

from settings_production import BaseConfig


class LocalConfig(BaseConfig):
    DEBUG = False

    # 生产新数据库
    # MYSQL_HOST = "192.168.13.39"
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "yan718844"
    MYSQL_DB = "devops"

    # 生产旧数据库
    # OLD_MYSQL_HOST = "192.168.13.39"
    MYSQL_HOST = "127.0.0.1"
    OLD_MYSQL_PORT = 3306
    OLD_MYSQL_USER = "root"
    OLD_MYSQL_PWD = "yan718844"
    OLD_MYSQL_DB = "jpushras"

    # 获取用户信息API,单个用户加上参数 ?user_ids=xxx
    USER_INFO = {
        'url': 'http://192.168.13.39:9555/user_center/v1/user/get_user_list',
        # 'url': 'http://127.0.0.1:8088/user_center/v1/user/get_user_list',
    }

    # 获取用户信息API，单个用户加上参数 ?user_ids=xxx
    USER_CENTER_API = {
        'user_url': 'http://192.168.13.39:9555/user_center/v1/user/get_user_list',
        'department_url': 'http://192.168.13.39:9555/user_center/v1/department/get_department_list'
    }

    # 获取部门信息API
    DEPARTMENT_INFO = {
        'url': 'http://192.168.13.39:9555/user_center/v1/user/get_user_list?department_id=',
        # 'url': 'http://127.0.0.1:8088/user_center/v1/user/get_user_list?department_id=',
    }

    IPORTAL_SESSIONID = {
        'url': 'http://192.168.13.39:7789/api/system/user/session',
    }

    # 本地运维平台redis信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 1
    REDIS_PWD = ""

    # VPN 测试环境
    VPN_IP_PORT = '183.232.40.166:8220'
    CERTIFICATE_DATA_PATH = r'D:\openvpn_cert'
    FAB_CMD = 'fab'

    # 发送邮件API
    EMAIL_API = 'http://192.168.13.39:7789/api/crm/send_email_api'

    # 工单待办任务URL
    # WORKFLOW_TASE = ('http://192.168.13.39:7789/spa/#/pages/plugin?url='
    #                  'L3BsdWdpbnNlcnZlci9vcHMvd29ya2Zsb3cvd29ya29yZGVyP2F'
    #                  'jdGlvbj1saXN0JmNsYXNzZmljYXRpb249dGFzaw==&_k=glyviy')
    WORKFLOW_TASE = ('http://127.0.0.1:7789/pluginserver/ops/workflow/workorder?'
                     'action=list&classfication=task')

    # web安装虚拟机伪终端参数
    INSTALL_VM = {
        # 'url': 'http://192.168.13.39:9955/pluginserver/butterfly/',
        'url': 'http://192.168.13.39:9975/pluginserver/butterfly/',
        'file_dir': '/opt/vm_web/install_file/',
        'cmd': ('export PYTHONOPTIMIZE=1 && cd /opt/vm_web/sys_manage/ '
                '&& /home/admin/venvs/butterfly/bin/python main.py vm'),
    }