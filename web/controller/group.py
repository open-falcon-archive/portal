# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'

from web import app
from flask import request, g, jsonify, render_template
from web.model.host_group import HostGroup
from web.model.grp_tpl import GrpTpl
from web.service import group_service
from frame.config import UIC_ADDRESS
from frame import config


@app.route('/group/create', methods=['POST'])
def group_create_post():
    grp_name = request.form['grp_name'].strip()
    if not grp_name:
        return jsonify(msg="group name is blank")

    grp_id = HostGroup.create(grp_name, g.user_name, 1)
    if grp_id > 0:
        return jsonify(msg='')
    else:
        return jsonify(msg='grp_name has already existent')


@app.route('/group/delete/<group_id>')
def group_delete_get(group_id):
    group_id = int(group_id)
    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group')

    if not group.writable(g.user_name):
        return jsonify(msg='no permission')

    return jsonify(msg=group_service.delete_group(group_id))


@app.route('/group/update/<group_id>', methods=['POST'])
def group_update_post(group_id):
    group_id = int(group_id)
    new_name = request.form['new_name'].strip()
    if not new_name:
        return jsonify(msg='new name is blank')

    group = HostGroup.read(where='id = %s', params=[group_id])
    if not group:
        return jsonify(msg='no such group')

    if not group.writable(g.user_name):
        return jsonify(msg='no permission')

    HostGroup.update_dict({'grp_name': new_name}, 'id=%s', [group_id])
    return jsonify(msg='')


@app.route('/group/advanced')
def group_advanced_get():
    return render_template('group/advanced.html', config=config)


@app.route('/group/rename', methods=['POST'])
def group_rename_post():
    old_str = request.form['old_str'].strip()
    new_str = request.form['new_str'].strip()
    if not old_str:
        return jsonify(msg='old is blank')

    return jsonify(msg=group_service.rename(old_str, new_str, g.user_name))


@app.route('/group/templates/<grp_id>')
def group_templates_get(grp_id):
    grp_id = int(grp_id)
    grp = HostGroup.read(where='id = %s', params=[grp_id])
    if not grp:
        return jsonify(msg='no such group')

    ts = GrpTpl.tpl_list(grp_id)

    return render_template('group/templates.html', group=grp, ts=ts, 
                            uic_address=UIC_ADDRESS['external'], config=config)


@app.route('/group/bind/template')
def group_bind_template_get():
    tpl_id = request.args.get('tpl_id', '').strip()
    grp_id = request.args.get('grp_id', '').strip()
    if not tpl_id:
        return jsonify(msg="tpl id is blank")

    if not grp_id:
        return jsonify(msg="grp id is blank")

    GrpTpl.bind(grp_id, tpl_id, g.user_name)
    return jsonify(msg='')
