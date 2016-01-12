# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'

import logging
import datetime
import urllib
from flask import Flask, request, g, session, make_response, redirect
from flask.ext.babel import Babel
from frame.api import uic

app = Flask(__name__)
app.config.from_object("frame.config")
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config.get('LANGUAGES').keys())

@babel.timezoneselector
def get_timezone():
    return app.config.get('BABEL_DEFAULT_TIMEZONE')

# config log
log_formatter = '%(asctime)s\t[%(filename)s:%(lineno)d] [%(levelname)s: %(message)s]'
log_level = logging.DEBUG if app.config['DEBUG'] else logging.WARNING
logging.basicConfig(format=log_formatter, datefmt="%Y-%m-%d %H:%M:%S", level=log_level)

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
    g.locale = get_locale()
    if 'user_name' in session and session['user_name']:
        g.user_name = session['user_name']
    else:
        sig = request.cookies.get('sig')
        if not sig:
            return redirect_to_sso()

        username = uic.username_from_sso(sig)
        if not username:
            return redirect_to_sso()

        session['user_name'] = username
        g.user_name = session['user_name']


def redirect_to_sso():
    sig = uic.gen_sig()
    resp = make_response(redirect(uic.login_url(sig, urllib.quote(request.url))))
    resp.set_cookie('sig', sig)
    return resp


from web.controller import home, group, plugin, host, expression, api, template, strategy, nodata, cluster
