# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
from flask import request


def remote_ip():
    if not request.headers.getlist("X-Forward-For"):
        return request.remote_addr
    else:
        return request.headers.getlist("X-Forward-For")[0]


def metric_query(query, limit=50):
    size = 0
    metrics = []
    with open('metrics') as f:
        for line in f.readlines():
            if query in line:
                metrics.append(line.strip())
                size += 1
                if size >= limit:
                    break

    return metrics