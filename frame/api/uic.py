# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
import requests
import logging

from frame.config import UIC_ADDRESS, UIC_TOKEN


def gen_sig():
    url = '%s/sso/sig' % UIC_ADDRESS['internal']
    return requests.get(url).content


def username_from_sso(sig=''):
    url = '%s/sso/user/%s?token=%s' % (UIC_ADDRESS['internal'], sig, UIC_TOKEN)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        return None

    js = r.json()
    if 'user' in js:
        return js['user']['name']

    return None


def login_url(sig='', callback=''):
    return UIC_ADDRESS['login']


def query_group(query='', limit=10):
    r = requests.get('%s/team/query' % UIC_ADDRESS['internal'],
                     params={'query': query, 'limit': limit, 'token': UIC_TOKEN})
    j = r.json()
    if 'msg' in j and j['msg']:
        return []
        logging.getLogger().error(
            'call %s fail. parameter:[query:%s, limit:%s] msg: %s' % (url_query_uic_group, query, limit, j['msg']))
    return j['teams']


def email_in_groups(email=None, groups=None):
    if not email or not groups:
        return False

    if '@' in email:
        email = email.split('@')[0]

    r = requests.get('%s/user/in' % UIC_ADDRESS['internal'],
                     params={'name': email, 'teams': groups, 'token': UIC_TOKEN})
    txt = r.text
    return txt == '1'


if __name__ == "__main__":
    print(username_from_sso())