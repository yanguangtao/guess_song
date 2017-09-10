#!/bin/env python
# -*-coding:utf-8-*-
from sqlalchemy import Column, String, Integer, DateTime, text
from common.sqlalchemy_ctl import Base
from common.utility import create_table
from conf import settings


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    id_type = Column(String(32), nullable=False, server_default='wx')
    openId = Column(String(128), nullable=False, server_default='')
    unionId = Column(String(128), nullable=False, server_default='')
    nickName = Column(String(128), nullable=False, server_default='')
    # 性别 0：未知、1：男、2：女
    phone = Column(String(32), nullable=False, server_default='')
    avatarUrl = Column(String(128), nullable=False, server_default='0')
    # 备注名可以修改的
    name = Column(String(128), nullable=False, server_default='')
    gender = Column(String(12), nullable=False, server_default='1')
    country = Column(String(128), nullable=False, server_default='')
    province = Column(String(128), nullable=False, server_default='')
    city = Column(String(128), nullable=False, server_default='')
    create_time = Column(DateTime(), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(DateTime(), nullable=False,
                         server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

if settings.CREATE_TABLE:
    create_table("user")