# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
from web import app
from flask import request, jsonify
from web.model.strategy import Strategy
from frame import config
from fe_api import post2FeUpdateEventCase
import logging
log = logging.getLogger(__name__)

@app.route('/strategy/update', methods=['POST'])
def strategy_update_post():
    sid = request.form['sid'].strip()
    metric = request.form['metric'].strip()
    tags = request.form['tags'].strip()
    max_step = request.form['max_step'].strip()
    priority = request.form['priority'].strip()
    note = request.form['note'].strip()
    func = request.form['func'].strip()
    op = request.form['op'].strip()
    right_value = request.form['right_value'].strip()
    run_begin = request.form['run_begin'].strip()
    run_end = request.form['run_end'].strip()
    tpl_id = request.form['tpl_id'].strip()
    data = {'id': sid}
    alarmAdUrl = config.JSONCFG['shortcut']['falconUIC'] + "/api/v1/alarmadjust/whenstrategyupdated"
    if not metric:
        return jsonify(msg='metric is blank')

    if not note:
        return jsonify(msg='note is blank')

    if metric == 'net.port.listen' and '=' not in tags:
        return jsonify(msg='if metric is net.port.listen, tags should like port=22')
    need_reset = False
    if sid:
        st = Strategy.get(sid)
        if (st.func != func or st.right_value != right_value or st.op != op or st.metric != metric or st.tags !=
                tags):
            need_reset = True
        log.debug("need_reset: " + str(need_reset))
        log.debug(str(st.to_json()))
    if sid:
        # update
        Strategy.update_dict(
            {
                'metric': metric,
                'tags': tags,
                'max_step': max_step,
                'priority': priority,
                'func': func,
                'op': op,
                'right_value': right_value,
                'note': note,
                'run_begin': run_begin,
                'run_end': run_end
            },
            'id=%s',
            [sid]
        )
        if need_reset:
            respCode = post2FeUpdateEventCase(alarmAdUrl, data)
            if respCode != 200:
                log.error(alarmAdUrl + " got " + str(respCode) + " with " + str(data))
        return jsonify(msg='')

    # insert
    Strategy.insert(
        {
            'metric': metric,
            'tags': tags,
            'max_step': max_step,
            'priority': priority,
            'func': func,
            'op': op,
            'right_value': right_value,
            'note': note,
            'run_begin': run_begin,
            'run_end': run_end,
            'tpl_id': tpl_id
        }
    )
    respCode = post2FeUpdateEventCase(alarmAdUrl, data)
    if respCode != 200:
        log.error(alarmAdUrl + " got " + str(respCode) + " with " + str(data))
    return jsonify(msg='')


@app.route('/strategy/<sid>')
def strategy_get(sid):
    sid = int(sid)
    s = Strategy.get(sid)
    if not s:
        return jsonify(msg='no such strategy')

    return jsonify(msg='', data=s.to_json())


@app.route('/strategy/delete/<sid>')
def strategy_delete_get(sid):
    sid = int(sid)
    s = Strategy.get(sid)
    data = {'id': sid}
    alarmAdUrl = config.JSONCFG['shortcut']['falconUIC'] + "/api/v1/alarmadjust/whenstrategydeleted"
    if not s:
        return jsonify(msg='no such strategy')

    Strategy.delete_one(sid)
    respCode = post2FeUpdateEventCase(alarmAdUrl, data)
    if respCode != 200:
        log.error(alarmAdUrl + " got " + str(respCode) + " with " + str(data))
    return jsonify(msg='')
