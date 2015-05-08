# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'

from web import app
from flask import render_template, request, g
from web.model.host_group import HostGroup
from frame import config


@app.route('/')
def home_get():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 10))
    query = request.args.get('q', '').strip()
    mine = request.args.get('mine', '1')
    me = g.user_name if mine == '1' else None
    vs, total = HostGroup.query(page, limit, query, me)
    return render_template(
        'group/index.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'mine': mine,
            'is_root': g.user_name in config.MAINTAINERS,
            'community': config.COMMUNITY,
        }
    )

