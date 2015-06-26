# -*- coding:utf-8 -*-
__author__ = 'niean'
from web import app
from flask import request, g, render_template, jsonify
from web.model.nodata import Nodata
from frame.params import required_chk
from frame.config import UIC_ADDRESS


@app.route('/nodatas')
def nodatas_get():
    g.menu = 'nodatas'
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 5))
    query = request.args.get('q', '').strip()
    mine = request.args.get('mine', '1')
    me = g.user_name if mine == '1' else None
    vs, total = Nodata.query(page, limit, query, me)
    return render_template(
        'nodata/list.html',
        data={
            'vs': vs,
            'total': total,
            'query': query,
            'limit': limit,
            'page': page,
            'mine': mine,
        }
    )

@app.route('/nodata/add')
def nodata_add_get():
    g.menu = 'nodatas'
    o = Nodata.get(int(request.args.get('id', '0').strip()))
    return render_template('nodata/add.html',
                           data={'nodata': o, 'uic_address': UIC_ADDRESS['external']})


@app.route('/nodata/update', methods=['POST'])
def nodata_update_post():
    nodata_id = request.form['nodata_id'].strip()
    endpoint = request.form['endpoint'].strip()
    metric = request.form['metric'].strip()
    tags = request.form['tags'].strip()
    dstype = request.form['dstype'].strip()
    step = request.form['step'].strip()
    mock = request.form['mock'].strip()
    cluster = request.form['cluster'].strip()

    msg = required_chk({
        'endpoint' : endpoint,
        'metric' : metric,
        'dstype' : dstype,
        'step' : step,
        'mock': mock,
        'cluster': cluster,
    })

    if msg:
        return jsonify(msg=msg)

    return jsonify(msg=Nodata.save_or_update(
        nodata_id,
        endpoint,
        metric,
        tags,
        dstype,
        step,
        mock,
        cluster,
        g.user_name,
    ))

@app.route('/nodata/delete/<nodata_id>')
def nodata_delete_get(nodata_id):
    nodata_id = int(nodata_id)
    Nodata.delete_one(nodata_id)
    return jsonify(msg='')
