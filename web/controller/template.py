# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
from web import app
from flask import g, render_template, request, jsonify
from web.model.template import Template
from web.model.strategy import Strategy
from web.model.action import Action
from web.model.grp_tpl import GrpTpl
from web.model.host_group import HostGroup
from frame.config import UIC_ADDRESS
from frame import config
from fe_api import post2FeUpdateEventCase
import logging
log = logging.getLogger(__name__)

@app.route('/templates')
def templates_get():
    g.menu = 'templates'
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 10))
    query = request.args.get('q', '').strip()
    mine = request.args.get('mine', '1')
    me = g.user_name if mine == '1' else None
    vs, total = Template.query(page, limit, query, me)
    for v in vs:
        v.parent = Template.get(v.parent_id)
    return render_template(
        'template/list.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'mine': mine,
            'uic_address': UIC_ADDRESS['external'],
        },
        config=config
    )


@app.route('/template/create', methods=['POST'])
def template_create_post():
    name = request.form['name'].strip()
    if not name:
        return jsonify(msg='name is blank')

    if Template.read('tpl_name=%s', [name]):
        return jsonify(msg='name already existent')

    tpl_id = Template.insert({'tpl_name': name, 'create_user': g.user_name})
    if tpl_id:
        return jsonify(msg='', id=tpl_id)

    return jsonify(msg='create fail')


@app.route('/template/update/<tpl_id>')
def template_update_get(tpl_id):
    g.menu = 'templates'
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    t.parent = Template.get(t.parent_id)
    ss = Strategy.select_vs(where='tpl_id = %s', params=[tpl_id], order='metric')
    t.action = Action.get(t.action_id)
    return render_template('template/update.html', 
            data={'tpl': t, 'ss': ss, 'uic': UIC_ADDRESS['external']}, config=config)


@app.route('/template/binds/<tpl_id>')
def template_binds_get(tpl_id):
    g.menu = 'templates'
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    groups = GrpTpl.grp_list(tpl_id)
    return render_template(
            'template/groups.html', 
            data={
                "gs": groups,
                "tpl": t,
                "uic_address": UIC_ADDRESS['external'],
            }, 
            config=config)


@app.route('/template/unbind/group')
def template_unbind_group_get():
    tpl_id = request.args.get('tpl_id', '')
    grp_id = request.args.get('grp_id', '')
    data = {'templateId': tpl_id, 'hostgroupId': grp_id}
    alarmAdUrl = config.JSONCFG['shortcut']['falconUIC'] + "/api/v1/alarmadjust/whentempleteunbind"
    if not tpl_id:
        return jsonify(msg="tpl_id is blank")

    if not grp_id:
        return jsonify(msg="grp_id is blank")

    GrpTpl.unbind(grp_id, tpl_id)
    respCode = post2FeUpdateEventCase(alarmAdUrl, data)
    if respCode != 200:
        log.error(alarmAdUrl + " got " + str(respCode) + " with " + str(data))
    return jsonify(msg='')


@app.route('/template/unbind/node')
def template_unbind_grp_name_get():
    tpl_id = request.args.get('tpl_id', '')
    if not tpl_id:
        return jsonify(msg="tpl_id is blank")

    grp_name = request.args.get('grp_name', '')
    if not grp_name:
        return jsonify(msg='grp_name is blank')

    hg = HostGroup.read('grp_name=%s', [grp_name])
    if not hg:
        return jsonify(msg='no such host group')

    GrpTpl.unbind(hg.id, tpl_id)
    return jsonify(msg='')


@app.route('/template/bind/node', methods=['POST'])
def template_bind_node_post():
    node = request.form['node'].strip()
    tpl_id = request.form['tpl_id'].strip()
    if not node:
        return jsonify(msg='node is blank')

    if not tpl_id:
        return jsonify(msg='tpl id is blank')

    hg = HostGroup.read('grp_name=%s', [node])
    if not hg:
        return jsonify(msg='no such node')

    GrpTpl.bind(hg.id, tpl_id, g.user_name)
    return jsonify(msg="")


@app.route('/template/view/<tpl_id>')
def template_view_get(tpl_id):
    g.menu = 'templates'
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    t.parent = Template.get(t.parent_id)
    ss = Strategy.select_vs(where='tpl_id = %s', params=[tpl_id], order='metric')
    t.action = Action.get(t.action_id)
    return render_template('template/view.html', 
            data={'tpl': t, 'ss': ss, 'uic_address': UIC_ADDRESS['external']}, config=config)


@app.route('/template/fork/<tpl_id>')
def template_fork_get(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    new_id = t.fork(g.user_name)
    if new_id == -1:
        return jsonify(msg='name[copy_of_%s] has already existent' % t.tpl_name)
    return jsonify(msg='', id=new_id)


@app.route('/template/help')
def template_help_get():
    g.menu = 'templates'
    contact = app.config['CONTACT']
    return render_template('template/help.html', contact=contact, config=config)


@app.route('/template/delete/<tpl_id>')
def template_delete_get(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    data = {'templateId': tpl_id}
    alarmAdUrl = config.JSONCFG['shortcut']['falconUIC'] + "/api/v1/alarmadjust/whentempletedeleted"
    if not t:
        return jsonify(msg='no such template')

    if not t.writable(g.user_name):
        return jsonify(msg='no permission')

    Template.delete_one(tpl_id)
    action_id = t.action_id
    if action_id:
        Action.delete_one(action_id)

    Strategy.delete('tpl_id = %s', [tpl_id])

    GrpTpl.unbind_tpl(tpl_id)
    respCode = post2FeUpdateEventCase(alarmAdUrl, data)
    if respCode != 200:
        log.error(alarmAdUrl + " got " + str(respCode) + " with " + str(data))
    return jsonify(msg='')


@app.route('/template/rename/<tpl_id>', methods=['POST'])
def template_rename_post(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    name = request.form['name'].strip()
    parent_id = request.form.get('parent_id', '')
    if not parent_id:
        parent_id = 0

    Template.update_dict({'tpl_name': name, 'parent_id': parent_id}, 'id=%s', [tpl_id])
    return jsonify(msg='')


@app.route('/template/action/update/<tpl_id>', methods=['POST'])
def template_action_update_post(tpl_id):
    tpl_id = int(tpl_id)
    t = Template.get(tpl_id)
    if not t:
        return jsonify(msg='no such template')

    uic = request.form['uic'].strip()
    url = request.form['url'].strip()
    callback = request.form['callback'].strip()
    before_callback_sms = request.form['before_callback_sms'].strip()
    before_callback_mail = request.form['before_callback_mail'].strip()
    after_callback_sms = request.form['after_callback_sms'].strip()
    after_callback_mail = request.form['after_callback_mail'].strip()

    if t.action_id > 0:
        # update
        Action.update_dict(
            {
                'uic': uic,
                'url': url,
                'callback': callback,
                'before_callback_sms': before_callback_sms,
                'before_callback_mail': before_callback_mail,
                'after_callback_sms': after_callback_sms,
                'after_callback_mail': after_callback_mail
            },
            'id=%s',
            [t.action_id]
        )
    else:
        # insert
        action_id = Action.insert({
            'uic': uic,
            'url': url,
            'callback': callback,
            'before_callback_sms': before_callback_sms,
            'before_callback_mail': before_callback_mail,
            'after_callback_sms': after_callback_sms,
            'after_callback_mail': after_callback_mail
        })
        if action_id <= 0:
            return jsonify(msg='insert action fail')

        Template.update_dict({'action_id': action_id}, 'id=%s', [t.id])
    return jsonify(msg='')
