# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 9:00
# @Author  : weikai
# @File    : redis.py
# @Software: PyCharm
import sys

import redis


class RedisDBConfig:
    HOST = '127.0.0.1'
    PORT = 6379
    DBID = 8


def operator(func):
    def gen_status(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return gen_status


class RedisUtil(object):
    def __init__(self):
        if not hasattr(RedisUtil, 'pool'):
            RedisUtil.create_pool()
        self._connection = redis.Redis(connection_pool=RedisUtil.pool)

    @staticmethod
    def create_pool():
        RedisUtil.pool = redis.ConnectionPool(
            host=RedisDBConfig.HOST,
            port=RedisDBConfig.PORT,
            db=RedisDBConfig.DBID)

    @operator
    def set_data(self, key, value, ex=None):
        return self._connection.set(key, value, ex=ex)

    @operator
    def get_data(self, key):
        return self._connection.get(key)

    @operator
    def del_data(self, key):
        return self._connection.delete(key)


if __name__ == '__main__':
    http = sys.argv[1]
    path = sys.argv[2]
    RedisUtil().set_data(http, path)
