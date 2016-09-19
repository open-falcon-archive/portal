# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'

# -- app config --
DEBUG = True

# -- db config --
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASS = "password"
DB_NAME = "falcon_portal"

# -- cookie config --
SECRET_KEY = "4e.5tyg8-u9ioj"
SESSION_COOKIE_NAME = "falcon-portal"
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30

UIC_ADDRESS = {
    'internal': 'http://127.0.0.1:1234',
    'external': 'http://127.0.0.1:1234',
    'login': 'http://127.0.0.1:1234/auth/login?callback=http://127.0.0.1:5050/',
}

UIC_TOKEN = ''

MAINTAINERS = ['root']
CONTACT = 'ulric.qin@gmail.com'

COMMUNITY = True

JSONCFG = {}
JSONCFG['shortcut'] = {}
JSONCFG['shortcut']['falconPortal']     = "http://127.0.0.1:5050"
JSONCFG['shortcut']['falconDashboard']  = "http://127.0.0.1:8081"
JSONCFG['shortcut']['grafanaDashboard'] = "http://127.0.0.1:3000"
JSONCFG['shortcut']['falconAlarm']      = "http://127.0.0.1:9912"
JSONCFG['shortcut']['falconUIC']        = "http://127.0.0.1:1234"

try:
    from frame.local_config import *
except Exception, e:
    print('level=warning msg="%s"' % e)
