#!/usr/bin/env python
# coding=utf-8
from os.path import abspath, dirname

from sanic import Sanic
from sanic.response import json, html
from jinja2 import Environment, PackageLoader, select_autoescape

from ProxyIP.database import RedisClient

app = Sanic()
redis_conn = RedisClient()
env = Environment(
    loader=PackageLoader('ProxyIP', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


@app.route("/")
async def index(request):
    return json({"Welcome": "This is a proxy pool system."})


@app.route("/pop")
async def pop_proxy(request):
    proxy = redis_conn.pop_proxy().decode("utf8")
    if proxy[:5] == "https":
        return json({"https": proxy})
    else:
        return json({"http": proxy})


@app.route("/get/<count:int>")
async def get_proxy(request, count):
    res = []
    for proxy in redis_conn.get_proxies(count):
        if proxy[:5] == "https":
            res.append({"https": proxy})
        else:
            res.append({"http": proxy})
    return json(res)


@app.route("/count")
async def count_all_proxies(request):
    count = redis_conn.count_all_proxies()
    return json({"count": str(count)})


@app.route("/count/<score:int>")
async def count_score_proxies(request, score):
    count = redis_conn.count_score_proxies(score)
    return json({"count": str(count)})


@app.route("/clear/<score:int>")
async def clear_proxies(request, score):
    if redis_conn.clear_proxies(score):
        return json({"Clear": "Successful"})
    return json({"Clear": "Score should >= 0 and <= 10"})


@app.route("/analysis")
async def analysis(request):
    template = env.get_template('analysis.html')
    data = redis_conn.get_statistics()
    data = [int(s) for s in data]
    return html(template.render(existed_proxies=data,))
