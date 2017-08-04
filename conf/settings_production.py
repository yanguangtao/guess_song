#!/bin/env python
# -*- coding:utf8 -*-


class BaseConfig(object):
    DEBUG = False
    CREATE_TABLE = True

    SESSION_URL = "http://iportal.jpushoa.com/api/system/get_user_session"

    # 生产新数据库
    MYSQL_HOST = "172.16.100.199"
    MYSQL_PORT = 6033
    MYSQL_USER = "jpush"
    MYSQL_PWD = "jpush_BvAQhZkHa0U"
    MYSQL_DB = "devops"

    # 生产旧运维平台数据库
    OLD_MYSQL_HOST = "172.16.100.199"
    OLD_MYSQL_PORT = 6033
    OLD_MYSQL_USER = "jpush"
    OLD_MYSQL_PWD = "jpush_BvAQhZkHa0U"
    OLD_MYSQL_DB = "jpushras"

    # 3小时后自动重连mysql
    MYSQL_CONNECT_TIMEOUT = 3 * 60 * 60

    # token
    # 7天有效期
    TOKEN_TIMEOUT = 7 * 24 * 60 * 60
    PRIVATE_KEY = '8834567812345678'

    # 获取用户信息API，单个用户加上参数 ?user_ids=xxx
    USER_CENTER_API = {
        'user_url': 'http://iportal.jpushoa.com/user_center/v1/user/get_user_list',
        'department_url': 'http://iportal.jpushoa.com/user_center/v1/department/get_department_list'
    }

    # 获取部门信息API
    DEPARTMENT_INFO = {
        'url': 'http://iportal.jpushoa.com/user_center/v1/user/get_user_list?department_id='
    }

    IPORTAL_SESSIONID = {
        'url': 'http://iportal.jpushoa.com/api/system/user/session',
    }

    # 运维平台redis信息
    REDIS_HOST = "wrasn.channel.jpushoa.com"
    REDIS_PORT = 16899
    REDIS_DB = 1
    REDIS_PWD = "Sys.Nj1Inf6o"

    # VPN证书
    VPN_IP_PORT = '183.232.57.10:8220'
    CERTIFICATE_DATA_PATH = r'/home/admin/projects/certificate_data'
    FAB_CMD = '/home/admin/venvs/devops/bin/fab'

    # monitor-ops，监听redis的发布
    MONITOR_URL = "127.0.0.1"
    MONITOR_PORT = "7776"

    # 只更新物理机信息
    ONLY_UPDATE_PM = False

    # 发送邮件API
    EMAIL_API = 'http://iportal.jpushoa.com/api/crm/send_email_api'

    # 工单待办任务URL
    WORKFLOW_TASE = ('http://iportal.jpushoa.com/spa/#/pages/plugin?redict=aHR0cDovL2lwb3J0Y'
                     'WwuanB1c2hvYS5jb20vcGx1Z2luc2VydmVyL29wcy93b3JrZmxvdy93b3Jrb3JkZXI%2FY'
                     'WN0aW9uPWxpc3QmY2xhc3NmaWNhdGlvbj10YXNr&url=L3BsdWdpbnNlcnZlci9vcHMvd29'
                     'ya2Zsb3cvd29ya29yZGVyP2FjdGlvbj1saXN0JmNsYXNzZmljYXRpb249Y3JlYXRl&_k=hr9nq7')

    # 云主机名列表
    CLOUD_SERVER = {"alihk": u"阿里云香港",
                    "jpush-qcloud-hk": u"青云香港",
                    "bjqcloud3": u"青云北京",
                    "gdqcloud": u"青云广东",
                    "shqcloud": u"青云上海",
                    "hkrjy": u"睿江云香港",
                    "cloud-aliyun-hd1-": u"阿里云华东1区",
                    "cloud-aliyun-hb-": u"阿里云华北区",
                    "cloud-aliyun-gd-": u"阿里云广东区",
                    "cloud-aliyun-hk-": u"阿里云香港",
                    "cloud-qcloud-bj-": u"北京青云",
                    "cloud-qcloud-sh-": u"上海青云",
                    "cloud-qcloud-hk-": u"香港青云",
                    "cloud-qcloud-gd-": u"广东青云",
                    "cloud-rjy-bj-": u"北京睿江云",
                    "cloud-rjy-hk-": u"香港睿江云",
                    "aliyun": u"阿里云",
                    "alihk": "",
                    "alicloud": "",
                    "qcloud": "",
                    "rjycloud": "",
                    "txcloud": ""
                    }

    # web安装虚拟机伪终端参数
    INSTALL_VM = {
        'url':  'http://iportal.jpushoa.com/pluginserver/butterfly/',
        'cmd': ('export PYTHONOPTIMIZE=1 && cd /opt/vm_web/sys_manage/ '
                '&& /home/admin/venvs/butterfly/bin/python main.py vm'),
    }

    VM_OPERATION = {
        'cmd': ('export PYTHONOPTIMIZE=1 && cd /opt/vm_web/sys_manage/ '
                '&& /home/admin/venvs/butterfly/bin/python main.py'),
    }

    # 故障工单处理人ID列表
    # 固定人员 陈响澎1428，李万彤1202 魏新俊151 张飞鹏83 黄永坚872 陈赛帅884
    HELPDESK_OPERATOR_IDS = [83, 151, 872, 1202, 1428, 884]

    # 邮件通知去受理故障工单，多个接收人逗号分隔
    HELPDESK_EMAIL = 'IT@jiguang.cn'

    # 物理机品牌(首字母大写)
    PHYSICAL_MACHINE_BRAND = ('Dell', 'Inspur', 'Huawei')