#!/bin/env python
# -*-coding:utf-8-*-

from hashlib import sha1
import json
import requests
from sqlalchemy import desc, inspect, func

from common import error_msg
from common.my_log import logger
from common.sqlalchemy_ctl import DBSession
from conf import settings


class BaseController(object):
    def __init__(self, model):
        self._model = model
        self.model = model
        self._ret, self._msg = error_msg.SUCCESS
        self._data = {}
        self._resp_json = ""
        self.db = DBSession()

    def _clean_value(self, value):
        if isinstance(value, (str, unicode)):
            return value.strip()
        return value

    def _result(self, ret_msg=None, data=None):
        if not ret_msg is None:
            self._ret, self._msg = ret_msg
        if not data is None:
            self._data = data
        self._resp_json = json.dumps({
            "ret": self._ret,
            "msg": self._msg,
            "data": self._data
            })
        return self._resp_json

    def _filter_value(self, kwargs):
        return filter(lambda x: (
            x != "metadata"
            and x != "id"
            and not x.startswith("_")
            and x in kwargs
        ), dir(self._model))

    def __encryption(self, value):
        # 明文sha1加密
        password = sha1(str(value).strip()).hexdigest()
        return password

    def do_filter(self, **kwargs):
        session = self.db
        if session is None:
            return None
        pk = kwargs.get("id", None)
        try:
            filter_obj = session.query(self._model)
            if pk is not None:
                return filter_obj.filter_by(id=pk)
            value = {k: self._clean_value(kwargs[k]) for k in self._filter_value(kwargs)}
            filter_obj = filter_obj.filter_by(**value)
            kv = kwargs.get("like", None)
            if kv is not None:
                k, v = kv.split("^")
                filter_obj = filter_obj.filter(getattr(self._model, k).like("%%%s%%" % v))
            id_list = kwargs.get("id_list", None)
            if id_list is not None:
                filter_obj = filter_obj.filter(getattr(self._model, "id").in_(id_list))
            filter_condition = kwargs.get('filter_condition', None)
            if filter_condition is not None:
                filter_obj = filter_obj.filter(filter_condition)
            return filter_obj
        except Exception as e:
            logger.error(u"查询%s出错. %s, %s" % (self._model.__tablename__, e, kwargs))
            return None

    def filter_item(self, **kwargs):
        session = self.db
        if session is None:
            return None, None
        start = int(kwargs.get("start", -1))
        end = int(kwargs.get("end", -1))
        pk = kwargs.get("id", None)
        try:
            filter_obj = self.do_filter(**kwargs)
            if not filter_obj:
                return None, None
            if pk:
                return filter_obj.first(), 1
            order_by = kwargs.get("order_by", None)
            order_method = kwargs.get("order_method", None)
            if order_by is None:
                filter_obj = filter_obj.order_by(desc("id"))
            else:
                if order_method == "desc":
                    filter_obj = filter_obj.order_by(desc(order_by))
                else:
                    filter_obj = filter_obj.order_by(order_by)
            if start == -1 and end == -1:
                data = filter_obj.all()
                return data, len(data)
            else:
                pk = self.get_model_pk()
                if pk is None:
                    return None, None
                return filter_obj[start:end], filter_obj.with_entities(func.count(pk)).scalar()
        except Exception as e:
            logger.error(u"查询%s出错. %s, %s" % (self._model.__tablename__, e, kwargs))
            return None, None

    def new_item(self, **kwargs):
        session = self.db
        if session is None:
            return False
        try:
            value = {k: self._clean_value(kwargs[k]) for k in self._filter_value(kwargs)}
            if 'password' in value:
                # sha1加密密码字符
                value['password'] = self.__encryption(value['password'])
            new_obj = self._model(**value)
            session.add(new_obj)
            return new_obj
        except Exception as e:
            logger.error(u"新建%s出错. %s, %s" % (self._model.__tablename__, e, kwargs))
            return False

    def update_item(self, **kwargs):
        session = self.db
        if session is None:
            return False
        try:
            value = {k: self._clean_value(kwargs[k]) for k in self._filter_value(kwargs)}
            if 'password' in value:
                # sha1加密密码字符
                value['password'] = self.__encryption(value['password'])
            filter_obj = self.do_filter(**kwargs)
            if filter_obj:
                filter_obj.update(value)
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            logger.error(u"修改%s出错. %s, %s" % (self._model.__tablename__, e, kwargs))
            return False

    def delete_item(self, **kwargs):
        session = self.db
        if session is None:
            return False
        try:
            filter_obj = self.do_filter(**kwargs)
            if filter_obj:
                filter_obj.delete()
                return True
            else:
                return False
        except Exception as e:
            logger.error(u"删除%s出错. %s, %s" % (self._model.__tablename__, e, kwargs))
            return False

    def id_match(self, session, _input, match_key, attribute_list=None):
        """
        将ID匹配到对应的可读字段
        :param session:
        :param _input:
        :param match_key:
        :param attribute_list: [(当前存在的属性，新建的属性),
            当前存在的属性，默认把当前属性名字填充到新建属性里面
        ]
        :return: True/False
        """
        if session is None or attribute_list is None:
            return False
        if not isinstance(_input, list):
            input = [_input]
        else:
            input = _input
        id_list = [getattr(i, match_key) for i in input]
        item_list, _ = self.filter_item(session=session, id_list=id_list)
        # id_list 里面所有ID 都不匹配，返回None，直接结束函数。否则后面的id_dict中的for循环报错
        if item_list is None:
            return True
        id_dict = {getattr(k, "id"): k for k in item_list}
        for item in input:
            for i in attribute_list:
                if not isinstance(i, list) and not isinstance(i, tuple):
                    attribute, new_attribute = i, i
                else:
                    attribute, new_attribute = i[0], i[1]
                setattr(item, new_attribute, getattr(
                        id_dict.get(getattr(item, match_key), None),
                        attribute, None))
        return True

    def conf_match(self, _input, key=None, new_key=None, attribute_list=None):
        """
        将_conf_%s字段转换成%s_name字段
        :param _input:
        :param key:
        :param new_key:
        :param attribute_list: [ (当前存在的属性，新建的属性),
            当前存在的属性, 默认把当前属性名字加后缀_name 填充新建的属性
        ]
        :return:
        """
        conf_attribute_list = list()
        if key is not None or new_key is not None:
            if not isinstance(key, list) and not isinstance(key, tuple):
                _key, _new_key = [key], [new_key]
            if len(_key) != len(_new_key):
                return False
            conf_attribute_list = zip(key, new_key)
        for i in attribute_list:
            if not isinstance(i, list) and not isinstance(i, tuple):
                conf_attribute_list.append((i, "%s_name" % i))
            else:
                conf_attribute_list.append(i)
        conf_dict = dict()
        for j in conf_attribute_list:
            conf_dict[j[0]] = {i[0]: i[1] for i in getattr(self._model, "_conf_%s" % j[0], [])}

        def _match(_input, _attribute_list):
            for i in _attribute_list:
                if hasattr(_input, i[0]) and not hasattr(_input, i[1]):
                    setattr(_input, i[1], conf_dict[i[0]].get(
                        getattr(_input, i[0]), None))
        if isinstance(_input, list):
            for i in _input:
                _match(i, conf_attribute_list)
        else:
            _match(_input, conf_attribute_list)

    def user_match(self, _input, match_key, attribute_list=None):
        """
        将user_id匹配到对应的user_name和user_email
        :param _input:
        :param match_key:
        :param attribute_list: [['match_attribute', 'new_attribute_name'],...]
        for example:
            match_user_info(
                orm对象列表,
                orm对象里面的user_id字段的名称,
                [("user_info的name字段", "需要添加的新字段名字")]
            match_user_info(
                _input,
                "user_id",
                [("name", "user_name"), ("email", "user_email")])
        这样的话, _input里面的对象会新建了 user_name 和 user_email 两个属性
        :return: True/False
        """

        user_info_list = self.get_user_info()
        if not user_info_list:
            return False
        user_info_dict = {i['user_id']: i for i in user_info_list}
        for i in _input:
            value = user_info_dict.get(getattr(i, match_key), {})
            for j in attribute_list:
                if isinstance(j, list) or isinstance(j, tuple):
                    key, attribute = j[0], j[1]
                else:
                    key, attribute = j, j
                setattr(i, attribute, value.get(key, ''))
        return True

    def get_model_pk(self):
        """
        获取model主键
        :return: Column
        """
        try:
            ins = inspect(self.model)
            return ins.primary_key[0]
        except Exception as e:
            logger.error("获取主键失败e" % e)
            return None


