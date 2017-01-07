# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'

import logging
import datetime
import urllib
from flask import Flask, request, g, session, make_response, redirect
from frame.api import uic

app = Flask(__name__)
app.config.from_object("frame.config")

# config log
log_formatter = 'time="%(asctime)s" level=%(levelname)s msg="%(message)s"'
log_level = logging.DEBUG if app.config['DEBUG'] else logging.WARNING
logging.basicConfig(format=log_formatter, datefmt="%Y-%m-%dT%H:%M:%S%z", level=log_level)

IGNORE_PREFIX = ['/api', '/static']


@app.template_filter('fmt_time')
def fmt_time_filter(value, pattern="%Y-%m-%d %H:%M"):
    if not value:
        return ''
    return datetime.datetime.fromtimestamp(value).strftime(pattern)


@app.teardown_request
def teardown_request(exception):
    from frame.store import db
    db.commit()


@app.before_request
def before_request():
    p = request.path
    for ignore_pre in IGNORE_PREFIX:
        if p.startswith(ignore_pre):
            return

    sig = request.cookies.get('sig')
    if not sig:
        return redirect_to_sso()
    elif 'user_name' not in g:
        username = uic.username_from_sso(sig)
        g.user_name = username


def redirect_to_sso():
    resp = make_response(redirect(uic.login_url()))
    return resp


from web.controller import home, group, plugin, host, expression, api, template, strategy, nodata, cluster
