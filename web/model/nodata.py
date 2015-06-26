# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
from .bean import Bean
from frame.config import MAINTAINERS
from frame.api import uic
import time


class Nodata(Bean):
    _tbl = 'mockcfg'
    _cols = 'id, endpoint, metric, tags, dstype, step, mock, creator, cluster, t_create, t_modify'

    def __init__(self, _id, endpoint, metric, tags, dstype, step, mock, creator, cluster,
                 t_create, t_modify):
        self.id = _id
        self.endpoint = endpoint
        self.metric = metric
        self.tags = tags
        self.dstype = dstype
        self.step = step
        self.mock = mock
        self.creator = creator
        self.cluster = cluster
        self.t_create = t_create
        self.t_modify = t_modify
 
    @classmethod
    def query(cls, page, limit, query, me=None):
        where = ''
        params = []

        if me is not None:
            where = 'creator = %s'
            params.append(me)

        if query:
            where += ' and ' if where else ''
            where += 'endpoint like %s'
            params.append('%' + query + '%')

        vs = cls.select_vs(where=where, params=params, page=page, limit=limit)
        total = cls.total(where=where, params=params)
        return vs, total

    @classmethod
    def save_or_update(cls, nodata_id, endpoint, metric, tags, dstype, step, mock, cluster, login_user):
        if nodata_id:
            return cls.update_nodata(nodata_id, endpoint, metric, tags, dstype, step, mock, cluster)
        else:
            return cls.insert_nodata(endpoint, metric, tags, dstype, step, mock, cluster, login_user)

    @classmethod
    def insert_nodata(cls, endpoint, metric, tags, dstype, step, mock, cluster, login_user):
        nodata_id = Nodata.insert({
            'endpoint' : endpoint,
            'metric' : metric,
            'tags' : tags,
            'dstype' : dstype,
            'step' : step,
            'mock': mock,
            'creator': login_user,
            'cluster': cluster,
            't_create': int(time.time())
        })

        if nodata_id:
            return ''

        return 'save nodata fail'

    @classmethod
    def update_nodata(cls, nodata_id, endpoint, metric, tags, dstype, step, mock, cluster):
        e = Nodata.get(nodata_id)
        if not e:
            return 'no such nodata config %s' % nodata_id

        Nodata.update_dict(
            {
                'endpoint' : endpoint,
                'metric' : metric,
                'tags' : tags,
                'dstype' : dstype,
                'step' : step,
                'mock': mock,
                'cluster': cluster,
            },
            'id=%s',
            [e.id]
        )
        return ''

    def writable(self, login_user):
        if self.creator == login_user:
            return True

        if login_user in MAINTAINERS:
            return True

        return True
