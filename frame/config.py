# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'

# -- app config --
DEBUG = True

# -- db config --
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASS = ""
DB_NAME = "falcon_portal"

# -- cookie config --
SECRET_KEY = "4e.5tyg8-u9ioj"
SESSION_COOKIE_NAME = "falcon-portal"
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30

UIC_ADDRESS = {
    'internal': 'http://127.0.0.1:8080',
    'external': 'http://11.11.11.11:8080',
}

MAINTAINERS = ['root']
CONTACT = 'ulric.qin@gmail.com'

COMMUNITY = True

try:
    from frame.local_config import *
except Exception, e:
    print "[warning] %s" % e
