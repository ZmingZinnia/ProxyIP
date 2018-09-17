#!/usr/bin/env python
# coding=utf-8

REQUEST_TIMEOUT = 15
REQUEST_DELAY = 0

REDIS_HOST = "104.248.14.149"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = "proxies:ranking"
REDIS_MAX_CONNECTION = 20

MAX_SCORE = 10
MIN_SCORE = 0
INIT_SCORE = 1

SANIC_HOST = "localhost"
SANIC_PORT = 3289
SANIC_ACCESS_LOG = True

VALIDATOR_BATCH_COUNT = 256
VALIDATOR_BASE_URL = "https://www.baidu.com/"
VALIDATOR_RUN_CYCLE = 2


CRAWLER_RUN_CYCLE = 10
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}
