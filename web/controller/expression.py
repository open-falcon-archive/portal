# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
from web import app
from flask import request, g, render_template, jsonify
from web.model.expression import Expression
from web.model.action import Action
from frame.params import required_chk
from frame.config import UIC_ADDRESS


@app.route('/expressions')
def expressions_get():
    g.menu = 'expressions'
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 6))
    query = request.args.get('q', '').strip()
    mine = request.args.get('mine', '1')
    me = g.user_name if mine == '1' else None
    vs, total = Expression.query(page, limit, query, me)
    for v in vs:
        v.action = Action.get(v.action_id)
    return render_template(
        'expression/list.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'mine': mine,
        }
    )


@app.route('/expression/delete/<expression_id>')
def expression_delete_get(expression_id):
    expression_id = int(expression_id)
    Expression.delete_one(expression_id)
    return jsonify(msg='')


@app.route('/expression/add')
def expression_add_get():
    g.menu = 'expressions'
    a = None
    o = Expression.get(int(request.args.get('id', '0').strip()))
    if o:
        a = Action.get(o.action_id)
    return render_template('expression/add.html',
                           data={'action': a, 'expression': o, 'uic_address': UIC_ADDRESS['external']})


@app.route('/expression/update', methods=['POST'])
def expression_update_post():
    expression_id = request.form['expression_id'].strip()
    expression = request.form['expression'].strip()
    func = request.form['func'].strip()
    op = request.form['op'].strip()
    right_value = request.form['right_value'].strip()
    uic_groups = request.form['uic'].strip()
    max_step = request.form['max_step'].strip()
    priority = int(request.form['priority'].strip())
    note = request.form['note'].strip()
    url = request.form['url'].strip()
    callback = request.form['callback'].strip()
    before_callback_sms = request.form['before_callback_sms']
    before_callback_mail = request.form['before_callback_mail']
    after_callback_sms = request.form['after_callback_sms']
    after_callback_mail = request.form['after_callback_mail']

    msg = required_chk({
        'expression': expression,
        'func': func,
        'op': op,
        'right_value': right_value,
    })

    if msg:
        return jsonify(msg=msg)

    if not max_step:
        max_step = 3

    if not priority:
        priority = 0

    return jsonify(msg=Expression.save_or_update(
        expression_id,
        expression,
        func,
        op,
        right_value,
        uic_groups,
        max_step,
        priority,
        note,
        url,
        callback,
        before_callback_sms,
        before_callback_mail,
        after_callback_sms,
        after_callback_mail,
        g.user_name,
    ))


@app.route('/expression/pause')
def expression_pause_get():
    expression_id = request.args.get("id", '')
    pause = request.args.get('pause', '')
    if not expression_id:
        return jsonify(msg='id is blank')

    if not pause:
        return jsonify(msg='pause is blank')

    e = Expression.get(expression_id)
    if not e:
        return jsonify('no such expression %s' % expression_id)

    Expression.update_dict({'pause': pause}, 'id=%s', [expression_id])
    return jsonify(msg='')


@app.route('/expression/view/<eid>')
def expression_view_get(eid):
    eid = int(eid)
    g.menu = 'expressions'
    a = None
    o = Expression.get(eid)
    if o:
        a = Action.get(o.action_id)
    else:
        return 'no such expression'
    return render_template('expression/view.html', data={'action': a, 'expression': o})
