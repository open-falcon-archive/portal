# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
from flask import jsonify, request, render_template, g, make_response
from web import app
from web.model.host_group import HostGroup
from web.model.group_host import GroupHost
from web.model.grp_tpl import GrpTpl
from web.model.host import Host
from web.model.template import Template
from frame import config
from fe_api import post2FeUpdateEventCase
import time
import logging
log = logging.getLogger(__name__)

@app.route('/group/<group_id>/hosts.txt')
def group_hosts_export(group_id):
    group_id = int(group_id)

    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group %s' % group_id)

    vs, _ = Host.query(1, 10000000, '', '0', group_id)
    names = [v.hostname for v in vs]
    response = make_response('\n'.join(names))
    response.headers["content-type"] = "text/plain"
    return response


@app.route('/group/<group_id>/hosts')
def group_hosts_list(group_id):
    g.xbox = request.args.get('xbox', '')
    group_id = int(group_id)

    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group %s' % group_id)

    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 10))
    query = request.args.get('q', '')
    maintaining = request.args.get('maintaining', '0')
    vs, total = Host.query(page, limit, query, maintaining, group_id)
    return render_template(
        'host/index.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'maintaining': maintaining,
            'group': group,
        },
        config=config
    )


@app.route('/host/remove', methods=['POST'])
def host_remove_post():
    group_id = int(request.form['grp_id'].strip())
    host_ids = request.form['host_ids'].strip()
    alarmAdUrl = config.JSONCFG['shortcut']['falconUIC'] + "/api/v1/alarmadjust/whenendpointunbind"
    GroupHost.unbind(group_id, host_ids)
    for host_id in host_ids.split(","):
        data = {'hostgroupId': group_id, 'hostId': host_id}
        respCode = post2FeUpdateEventCase(alarmAdUrl, data)
        if respCode != 200:
            log.error(alarmAdUrl + " got " + str(respCode) + " with " + str(data))
            return jsonify(msg='delete host is failed , please try again!')
    return jsonify(msg='')


@app.route('/host/maintain', methods=['POST'])
def host_maintain_post():
    begin = int(request.form['begin'].strip())
    end = int(request.form['end'].strip())
    host_ids = request.form['host_ids'].strip()
    alarmAdUrl = config.JSONCFG['shortcut']['falconUIC'] + "/api/v1/alarmadjust/whenendpointonmaintain"
    if begin <= 0 or end <= 0:
        return jsonify(msg='begin or end is invalid')
    for host_id in host_ids.split(","):
        data = {'hostId': host_id, 'maintainBegin': begin, 'maintainEnd': end}
        respCode = post2FeUpdateEventCase(alarmAdUrl, data)
        if respCode != 200:
            log.error(alarmAdUrl + " got " + str(respCode) + " with " + str(data))
    return jsonify(msg=Host.maintain(begin, end, host_ids))


# 取消maintain时间
@app.route('/host/reset', methods=['POST'])
def host_reset_post():
    host_ids = request.form['host_ids'].strip()
    return jsonify(msg=Host.no_maintain(host_ids))


@app.route('/host/add')
def host_add_get():
    group_id = request.args.get('group_id', '')
    if not group_id:
        return jsonify(msg='no group_id given')

    group_id = int(group_id)
    group = HostGroup.read('id = %s', [group_id])
    if not group:
        return jsonify(msg='no such group')

    return render_template('host/add.html', group=group, config=config)


@app.route('/host/add', methods=['POST'])
def host_add_post():
    group_id = request.form['group_id']
    if not group_id:
        return jsonify(msg='no group_id given')

    group_id = int(group_id)
    group = HostGroup.read('id = %s', [group_id])
    if not group:
        return jsonify(msg='no such group')

    hosts = request.form['hosts'].strip()
    if not hosts:
        return jsonify(msg='hosts is blank')

    host_arr = hosts.splitlines()
    safe_host_arr = [h for h in host_arr if h]
    if not safe_host_arr:
        return jsonify(msg='hosts is blank')

    success = []
    failure = []

    for h in safe_host_arr:
        msg = GroupHost.bind(group_id, h)
        if not msg:
            success.append('%s<br>' % h)
        else:
            failure.append('%s %s<br>' % (h, msg))

    data = '<div class="alert alert-danger" role="alert">failure:<hr>' + ''.join(
        failure) + '</div><div class="alert alert-success" role="alert">success:<hr>' + ''.join(success) + '</div>'

    return jsonify(msg='', data=data)


# 展示某个机器bind的group
@app.route('/host/<host_id>/groups')
def host_groups_get(host_id):
    host_id = int(host_id)
    h = Host.read('id = %s', params=[host_id])
    if not h:
        return jsonify(msg='no such host')

    group_ids = GroupHost.group_ids(h.id)
    groups = [HostGroup.read('id = %s', [group_id]) for group_id in group_ids]
    return render_template('host/groups.html', groups=groups, host=h, config=config)


@app.route('/host/<host_id>/templates')
def host_templates_get(host_id):
    host_id = int(host_id)

    h = Host.read('id = %s', params=[host_id])
    if not h:
        return jsonify(msg='no such host')

    group_ids = GroupHost.group_ids(h.id)

    templates = GrpTpl.tpl_set(group_ids)
    for v in templates:
        v.parent = Template.get(v.parent_id)
    return render_template('host/templates.html', config=config, **locals())


@app.route('/host/unbind')
def host_unbind_get():
    host_id = request.args.get('host_id', '').strip()
    data = {'hostgroupId': group_id, 'hostId': host_id}
    alarmAdUrl = config.JSONCFG['shortcut']['falconUIC'] + "/api/v1/alarmadjust/whenendpointunbind"
    if not host_id:
        return jsonify(msg='host_id is blank')

    group_id = request.args.get('group_id', '').strip()
    if not group_id:
        return jsonify(msg='group_id is blank')

    GroupHost.unbind(int(group_id), host_id)
    respCode = post2FeUpdateEventCase(alarmAdUrl, data)
    if respCode != 200:
        log.error(alarmAdUrl + " got " + str(respCode) + " with " + str(data))
    return jsonify(msg='')
