#!/bin/env python
# -*-coding:utf-8-*-

from sqlalchemy import Column, String, Integer, DateTime, text
from common.sqlalchemy_ctl import Base
from common.utility import create_table
from conf import settings


class OnBattleRecordModel(Base):
    __tablename__ = 'on_battle_record'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer(), nullable=False, server_default='0')
    # 段位0青铜, 1白银, 2黄金, 3铂金, 4钻石, 5王者
    rank = Column(Integer(), nullable=False, server_default='0')
    # 几星, 默认0
    star = Column(Integer(), nullable=False, server_default='0')
    # rank分数
    rank_score = Column(Integer(), nullable=False, server_default='0')
    # 胜利场次
    win_num = Column(Integer(), nullable=False, server_default='0')
    # 失败场次
    lose_num = Column(Integer(), nullable=False, server_default='0')
    # 猜对歌曲总数
    right_num = Column(Integer(), nullable=False, server_default='0')
    # 未猜对总数
    error_num = Column(Integer(), nullable=False, server_default='0')
    Column(Integer(), nullable=False, server_default='0')
    create_time = Column(DateTime(), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(DateTime(), nullable=False,
                         server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

if settings.CREATE_TABLE:
    create_table("on_battle_record")