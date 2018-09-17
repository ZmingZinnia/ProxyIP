#!/usr/bin/env python
# coding=utf-8

import asyncio

import aiohttp

from .config import HEADERS, REQUEST_TIMEOUT, REQUEST_DELAY
from .validator import validator
from .logger import logger


LOOP = asyncio.get_event_loop()


async def _get_page(url, sleep):
    """
    Gets and returns the page content
    """
    async with aiohttp.ClientSession() as session:
        try:
            await asyncio.sleep(sleep)
            async with session.get(
                url, headers=HEADERS, timeout=REQUEST_TIMEOUT
            ) as resp:
                return await resp.text()
        except Exception:
            return ""


def requests(url, sleep=REQUEST_DELAY):
    """
    Request method, used for fetch the page content

    :param url
    :param sleep: delay time
    """
    html = LOOP.run_until_complete(asyncio.gather(_get_page(url, sleep)))
    if html:
        return "".join(html)


def test_proxy(proxy):
    """
    """
    cocou = validator.test_one_proxy(proxy)
    res = LOOP.run_until_complete(asyncio.gather(cocou))
    return res[0]
