# -*- coding:utf-8 -*-
__author__ = ['Ulric Qin', 'Eagle Liut']

from decouple import config

# -- app config --
DEBUG = config('FALCON_DEBUG', default=False, cast=bool)

# -- db config --

DB_HOST = config('FALCON_PORTAL_DB_HOST', default="127.0.0.1")
DB_PORT = config('FALCON_PORTAL_DB_PORT', default=3306, cast=int)
DB_USER = config('FALCON_PORTAL_DB_USER', default="root")
DB_PASS = config('FALCON_PORTAL_DB_PASS', default="password")
DB_NAME = config('FALCON_PORTAL_DB_NAME', default="falcon_portal")

# -- cookie config --
SECRET_KEY = config('FALCON_SECRET_KEY', default="4e.5tyg8-u9ioj")
SESSION_COOKIE_NAME = config('FALCON_SESSION_COOKIE_NAME', default="falcon-portal")
SESSION_COOKIE_DOMAIN = config('FALCON_SESSION_COOKIE_DOMAIN', default=None)
SERVER_NAME = config('FALCON_SERVER_NAME', default=None)
PERMANENT_SESSION_LIFETIME = config('FALCON_SESSION_LIFETIME', default=86400, cast=int)

URL_PORTAL = config('FALCON_URL_PORTAL', default="http://127.0.0.1:5050")
URL_DARSHBOARD = config('FALCON_URL_DARSHBOARD', default="http://127.0.0.1:8081")
URL_GRAFANA = config('FALCON_URL_GRAFANA', default="http://127.0.0.1:3000")
URL_ALARM = config('FALCON_URL_ALARM', default="http://127.0.0.1:9912")
URL_UIC = config('FALCON_URL_UIC', default="http://127.0.0.1:1234")

UIC_ADDRESS = {
    'internal': config('FALCON_UIC_INTERNAL', default='http://127.0.0.1:1234'),
    'external': config('FALCON_UIC_EXTERNAL', default=URL_UIC),
    'login': config(
        'FALCON_UIC_LOGIN',
        default='{}/auth/login?callback={}'.format(URL_UIC, URL_PORTAL)),
}

UIC_TOKEN = config('FALCON_UIC_TOKEN', default='')

MAINTAINERS = config('FALCON_MAINTAINERS', default='root').split(',')
CONTACT = config('FALCON_CONTACT', default='ulric.qin@gmail.com')

COMMUNITY = True

JSONCFG = {}
JSONCFG['shortcut'] = {}
JSONCFG['shortcut']['falconPortal'] = URL_PORTAL
JSONCFG['shortcut']['falconDashboard'] = URL_DARSHBOARD
JSONCFG['shortcut']['grafanaDashboard'] = URL_GRAFANA
JSONCFG['shortcut']['falconAlarm'] = URL_ALARM
JSONCFG['shortcut']['falconUIC'] = URL_UIC

try:
    from frame.local_config import *
except Exception, e:
    print('level=warning msg="%s"' % e)
