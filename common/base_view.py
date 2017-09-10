#!/bin/env python
# -*- coding:utf8 -*-

import json
import time
import requests

from flask import request, Response, render_template, abort
from sqlalchemy_ctl import DBSession

from common.my_log import logger
from common import utility
from common import error_msg

from conf import settings


class BaseView(object):
    def __init__(self, **kwargs):
        controller_obj = kwargs.get("controller_obj", None)
        if controller_obj != None:
            del kwargs["controller_obj"]
        self._restful = kwargs.get("restful", False)
        self._db_session = DBSession()
        self._user = None
        self._ret, self._msg = error_msg.SUCCESS
        self._data = {}
        self._resp_json = ""
        self._input = kwargs
        self._controller_obj = controller_obj
        self.__start_time = time.time()

    def dispatch(self):
        self.get_input_arguments()
        self._input["session"] = self._db_session
        if request.method == "GET":
            action = self._input.get("action", None)
            if action:
                func = getattr(self, "get_action_%s" % action, None)
                if func:
                    return func()
                else:
                    return render_template("404.html")
            else:
                return self.get()
        elif request.method == "POST":
            action = self._input.get("action", None)
            if action:
                func = getattr(self, "post_action_%s" % action, None)
                if func:
                    return func()
                else:
                    return render_template("404.html")
            else:
                return self.post()
        elif request.method == "PUT":
            return self.put()
        elif request.method == "DELETE":
            return self.delete()
        return self._response(error_msg.PARAMS_ERROR)

    def get(self,
            must_input=None,
            enable_input=None,
            disable_input=None,
            disable_output=None):

        if not self.check_input_arguments(must_input, enable_input, disable_input):
            return self._response(error_msg.PARAMS_ERROR)
        if self._controller_obj is not None:
            if self._do_get(disable_output=disable_output):
                self._ret, self._msg = error_msg.SUCCESS
                self._db_session.commit()
            else:
                self._ret, self._msg = error_msg.SERVER_ERROR
                self._db_session.rollback()
            return self._response()
        else:
            self._ret, self._msg = error_msg.SERVER_ERROR
            return self._response()

    def _do_get(self, disable_output=None, transform_json=True):
        try:
            data, total = self._controller_obj.filter_item(**self._input)
            self._data["total"] = total
            if transform_json:
                self._data["list"] = utility.to_dict_obj(data, without_fields=disable_output)
            else:
                self._data["list"] = data
            return True
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error("get method error: %s" % e)
            return False

    def post(self,
             must_input=None,
             enable_input=None,
             disable_input=None):
        if not self.check_input_arguments(must_input, enable_input, disable_input):
            return self._response(error_msg.PARAMS_ERROR)
        if self._controller_obj is not None:
            if self._do_post():
                self._ret, self._msg = error_msg.SUCCESS
            else:
                self._ret, self._msg = error_msg.SERVER_ERROR
            return self._response()
        else:
            self._ret, self._msg = error_msg.SERVER_ERROR
            return self._response()

    def _do_post(self):
        try:
            if self._controller_obj.new_item(**self._input):
                self._db_session.commit()
                return True
            else:
                self._db_session.rollback()
                logger.error("post method error")
                return False
        except Exception as e:
            self._ret, self._msg = error_msg.SERVER_ERROR
            logger.error("post method error: %s" % e)
            return False

    def put(self,
            must_input=None,
            enable_input=None,
            disable_input=None):
        if not self.check_input_arguments(must_input, enable_input, disable_input):
            return self._response(error_msg.PARAMS_ERROR)
        if self._controller_obj is not None:
            if self._do_put():
                self._ret, self._msg = error_msg.SUCCESS
            else:
                self._ret, self._msg = error_msg.SERVER_ERROR
            return self._response()
        else:
            self._ret, self._msg = error_msg.SERVER_ERROR
            return self._response()

    def _do_put(self):
        try:
            if self._controller_obj.update_item(**self._input):
                self._db_session.commit()
                return True
            else:
                self._db_session.rollback()
                return False
        except Exception as e:
            logger.error("put method error: %s" % e)
            return False

    def delete(self,
               must_input=None,
               enable_input=None,
               disable_input=None):
        if not self.check_input_arguments(must_input, enable_input, disable_input):
            return self._response(error_msg.PARAMS_ERROR)
        if self._controller_obj is not None:
            if self._do_delete():
                self._ret, self._msg = error_msg.SUCCESS
            else:
                self._ret, self._msg = error_msg.SERVER_ERROR
            return self._response()
        else:
            self._ret, self._msg = error_msg.SERVER_ERROR
            return self._response()

    def _do_delete(self):
        try:
            if self._controller_obj.delete_item(**self._input):
                self._db_session.commit()
                return True
            else:
                self._db_session.rollback()
                logger.error("delete method error")
                return False
        except Exception as e:
            self._db_session.rollback()
            logger.error("delete method error: %s" % e)
            return False

    def check_session(self):
        session = request.cookies.get("session_id", "")
        if session and self.decode_session(session):
            return True
        return False

    def decode_session(self, session):
        try:
            data = requests.get("%s?sessionid=%s" % (settings.SESSION_URL, session)).json()
            if data["ret"] == 0:
                self._user = data["data"]
                return True
            else:
                return False
        except Exception as e:
            logger.error("get session error %s" % e)
            return False

    def _response(self, ret_msg=None, data=None):
        if not ret_msg is None:
            self._ret, self._msg = ret_msg
        if not data is None:
            self._data = data
        self._resp_json = json.dumps({
            "ret": self._ret,
            "msg": self._msg,
            "data": self._data
            })
        self._db_session.close()
        # if self._restful and self._ret != 0:
        #     return abort(error_msg.RET_CODE_MAP.get(self._ret, 500))
        return self._resp_json

    def set_input_arguments(self, key, value):
        self._input[key] = str(value)


