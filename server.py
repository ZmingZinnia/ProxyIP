#!/usr/bin/env python
# coding=utf-8

from ProxyIP.webapi import app
from ProxyIP.config import SANIC_HOST, SANIC_PORT, SANIC_ACCESS_LOG


# start web app
app.run(host=SANIC_HOST, port=SANIC_PORT, access_log=SANIC_ACCESS_LOG)
