#!/bin/env python
# -*-coding:utf-8-*-

import importlib

from flask import Flask, url_for
from flask_script import Manager, Shell, Server

from common.sqlalchemy_ctl import DBSession

import restful_urls

# modules 模块名称列表
modules = [

]

app = Flask(__name__, static_url_path='/pluginserver/ops/static')

def dispatch(item, restful=False):
    def _dispatch(**kwargs):
        obj = item[1]
        kwargs["controller_obj"] = item[2]
        kwargs["restful"] = restful
        return obj(**kwargs).dispatch()
    return _dispatch

methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]

for i in modules:
    for j in getattr(importlib.import_module('%s.urls' % i), 'urls'):
        url_prefix = "/%s/%s" % (i, j[0])
        app.add_url_rule(url_prefix, url_prefix, dispatch(j), methods=methods)

for i in restful_urls.urls:
    _methods = methods
    if len(i) == 4:
        _methods = i[3]
    url_prefix = "/%s" % i[0]
    app.add_url_rule(url_prefix, url_prefix, dispatch(i, True), methods=_methods)


def _make_shell_context():
    return {'app': app, 'dbsession': DBSession()}

manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_shell_context))
manager.add_command("runserver", Server(host="0.0.0.0", port=7789, use_debugger=True))


@manager.command
def list_routes():
    """ a helper method to list routes.
        usage:  python server.py list_routes
    """
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, ','.join(rule.methods), url))
        output.append(line)
    for line in sorted(output):
        print line

if __name__ == '__main__':
    manager.run()
