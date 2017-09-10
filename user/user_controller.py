#!/bin/env python
# -*-coding:utf-8-*-
from common.base_controller import BaseController
from common.utility import to_dict_obj
from user.user_model import UserModel


class UserController(BaseController):
    def login(self, data):
        open_id = data.get("openId", None)
        print data
        if not open_id:
            self._ret, self._msg = 1, "不正确"
            return self._result()
        user, total = self.filter_item(openId=open_id)

        if user:
            user = user[0]
            try:
                user_exist = self.update_item(id=user.id, **data)
                self.db.commit()
                self.db.flush()
            except Exception as e:
                print e
        else:
            try:
                user = self.new_item(**data)
                self.db.commit()
                self.db.flush()
            except Exception as e:
                print e

        return to_dict_obj(user)



user_controller = UserController(UserModel)