#!/usr/bin/env python
# coding=utf-8

import random

import redis

from .config import (
    REDIS_KEY,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_HOST,
    REDIS_MAX_CONNECTION,
    MAX_SCORE,
    MIN_SCORE,
    INIT_SCORE,
)


class RedisClient:
    """
    The proxy pool relies on the Redis database, using the data structure of
    its ordered collection.
    Can be sorted by score, key values cannot be repeated.
    """

    def __init__(
        self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD
    ):
        conn_pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=password,
            max_connections=REDIS_MAX_CONNECTION,
        )
        self.redis = redis.Redis(connection_pool=conn_pool)

    def add_proxy(self, proxy, score=INIT_SCORE):
        """
        add a new proxy, init score, and ensure
        Add an agent, initialize the score INIT_SCORE < MAX_SCORE,
        ensure that the agent is acquired before the validator is
        run after the collector runs, resulting in the fact that
        the score is an unverified and unavailable agent

        :param proxy
        :param score
        """
        if not self.redis.zscore(REDIS_KEY, proxy):
            self.redis.zadd(REDIS_KEY, proxy, score)

    def reduce_proxy_score(self, proxy):
        """
        invalid, reduce score

        :param proxy: verify the proxy
        """
        score = self.redis.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            self.redis.zincrby(REDIS_KEY, proxy, -1)
        else:
            self.redis.zrem(REDIS_KEY, proxy)

    def increase_proxy_score(self, proxy):
        """
        valid, add score

        :param proxy: verify the proxy
        """
        score = self.redis.zscore(REDIS_KEY, proxy)
        if score and score < MAX_SCORE:
            self.redis.zincrby(REDIS_KEY, proxy, 1)

    def pop_proxy(self):
        """
        return a proxy
        """
        # The first attempt to get the highest score
        first_chance = self.redis.zrangebyscore(
            REDIS_KEY, MAX_SCORE, MAX_SCORE
        )
        if first_chance:
            return random.choice(first_chance)

        else:
            # The second time, try to take any proxies with a score of 7-10
            second_chance = self.redis.zrangebyscore(
                REDIS_KEY, MAX_SCORE - 3, MAX_SCORE
            )
            if second_chance:
                return random.choice(second_chance)
            # whatever
            else:
                last_chance = self.redis.zrangebyscore(
                    REDIS_KEY, MIN_SCORE, MAX_SCORE
                )
                if last_chance:
                    return random.choice(last_chance)

    def get_proxies(self, count=1):
        """
        Returns the specified number of proxies, with scores
        ordered from high to low.

        :param count: number of proxies
        """
        proxies = self.redis.zrevrange(REDIS_KEY, 0, count - 1)
        for proxy in proxies:
            yield proxy.decode("utf-8")

    def count_all_proxies(self):
        """
        Returns the total number of all proxies
        """
        return self.redis.zcard(REDIS_KEY)

    def count_score_proxies(self, score):
        """
        Returns the total number of specified score proxies

        :param score
        """
        if 0 <= score <= 10:
            proxies = self.redis.zrangebyscore(REDIS_KEY, score, score)
            return len(proxies)
        return -1

    def clear_proxies(self, score):
        """
        remove proxies that score below 'score'
        """
        if 0 <= score <= 10:
            proxies = self.redis.zrangebyscore(REDIS_KEY, 0, score)
            for proxy in proxies:
                self.redis.zrem(REDIS_KEY, proxy)
            return True
        return False

    def all_proxies(self):
        """
        return all proxyies
        """
        return self.redis.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
