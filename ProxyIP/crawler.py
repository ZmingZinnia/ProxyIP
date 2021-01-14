#!/usr/bin/env python
# coding=utf-8

import re

import pyquery

from .utils import requests, test_proxy
from .database import RedisClient
from .logger import logger


redis_conn = RedisClient()
all_funcs = []


def collect_funcs(func):
    """
    Decorator for collecting crawler functions
    """
    all_funcs.append(func)
    return func


class Crawler:

    @staticmethod
    def run():
        """
        start spider
        """
        logger.info("Crawler working...")
        for func in all_funcs:
            for proxy in func():
                if test_proxy(proxy):
                    redis_conn.add_proxy(proxy)
                    logger.info("Crawler √ {}".format(proxy))
        logger.info("Crawler resting...")

    @staticmethod
    @collect_funcs
    def crawl_66ip():
        """
        66ip proxy：http://www.66ip.cn
        """
        url = (
            "http://www.66ip.cn/nmtq.php?getnum=100&isp=0"
            "&anonymoustype=0&area=0&proxytype={}&api=66ip"
        )
        pattern = "\d+\.\d+.\d+\.\d+:\d+"

        items = [(0, "http://{}"), (1, "https://{}")]
        for item in items:
            proxy_type, host = item
            html = requests(url.format(proxy_type))
            if html:
                for proxy in re.findall(pattern, html):
                    yield host.format(proxy)


    @staticmethod
    @collect_funcs
    def crawl_kuaidaili():
        """
        kdl ：https://www.kuaidaili.com
        """
        url = "https://www.kuaidaili.com/free/{}"

        items = ["inha/1/"]
        for proxy_type in items:
            html = requests(url.format(proxy_type))
            if html:
                doc = pyquery.PyQuery(html)
                for proxy in doc(".table-bordered tr").items():
                    ip = proxy("[data-title=IP]").text()
                    port = proxy("[data-title=PORT]").text()
                    if ip and port:
                        yield "http://{}:{}".format(ip, port)

    @staticmethod
    @collect_funcs
    def crawl_ip3366():
        """
        ip3366 ：http://www.ip3366.net
        """
        url = "http://www.ip3366.net/?stype=1&page={}"

        items = [p for p in range(1, 8)]
        for page in items:
            html = requests(url.format(page))
            if html:
                doc = pyquery.PyQuery(html)
                for proxy in doc(".table-bordered tr").items():
                    ip = proxy("td:nth-child(1)").text()
                    port = proxy("td:nth-child(2)").text()
                    schema = proxy("td:nth-child(4)").text()
                    if ip and port and schema:
                        yield "{}://{}:{}".format(schema.lower(), ip, port)


crawler = Crawler()
