#!/usr/bin/env python
# coding=utf-8

import time

import schedule

from .config import CRAWLER_RUN_CYCLE, VALIDATOR_RUN_CYCLE

from .crawler import crawler
from .validator import validator
from .logger import logger


def run_schedule():
    """
    Start client
    """

    # Start spider
    schedule.every(CRAWLER_RUN_CYCLE).minutes.do(crawler.run)

    # Start valider
    schedule.every(VALIDATOR_RUN_CYCLE).minutes.do(validator.run)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("You have canceled all jobs")
            return
