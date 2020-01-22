# -*- coding: utf-8 -*-
# @Time    : 2020/1/22 9:37
# @Author  : weikai
# @File    : mysql.py
# @Software: PyCharm
import json
import pymysql
from datetime import *
from decimal import Decimal
import time


def db_singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args, **kw):
        t = str(cls) + args[0]['db_name'] + args[0]['host']
        if t not in instances:
            instances[t] = cls(*args, **kw)
        return instances[t]

    return _singleton


@db_singleton
class MysqlDb(object):
    def __init__(self, conf):
        self._host = conf.get('host')
        self._db_name = conf.get('db_name')
        self._db_username = conf.get('db_username')
        self._db_password = conf.get('db_password')
        self._db_port = conf.get('db_port')
        self._db_conn = pymysql.connect(host=self._host,
                                        port=self._db_port,
                                        user=self._db_username,
                                        password=self._db_password,
                                        autocommit=True,
                                        db=self._db_name,
                                        cursorclass=pymysql.cursors.DictCursor)

    def assemble_query(self, table, *args, **kwargs):
        keys = "*"
        if isinstance(keys, (tuple, list)):
            keys = ','.join(map(str, keys))
        sql = 'select %s ' % keys
        sql += ' from %s ' % table
        if kwargs:
            sql += ' where %s ' % Dict2Str(kwargs, 'and')
        #  sql
        sql = sql.replace("=None", " IS NULL")
        for x in args:
            sql = sql + ' ' + x
        return self.query(sql)

    def assemble_update(self, table, *args, **kwargs):
        sql = 'update %s   ' % table
        if kwargs:
            sql += ' set %s ' % Dict2Str(kwargs, ',')
        #  sql
        sql = sql.replace("=None", " = NULL")
        for x in args:
            sql = sql + ' ' + x
        return self.execute_sql_string(sql)

    def assemble_delete(self, table, *args, **kwargs):
        sql = 'delete from %s' % table
        if kwargs:
            sql += ' where %s ' % Dict2Str(kwargs, 'and')
        #  sql
        sql = sql.replace("=None", " IS NULL")
        for x in args:
            sql = sql + ' ' + x
        return self.execute_sql_string(sql)

    @staticmethod
    def assemble_query_sql(table, *args, **kwargs):
        keys = "*"
        if isinstance(keys, (tuple, list)):
            keys = ','.join(map(str, keys))
        sql = 'select %s ' % keys
        sql += ' from %s ' % table
        if kwargs:
            sql += ' where %s ' % Dict2Str(kwargs, 'and')
        #  sql
        sql = sql.replace("=None", " IS NULL")
        for x in args:
            sql = sql + ' ' + x
        return sql

    def query(self, sqlStatement):
        """
        mysql查询方法
        :param sqlStatement: sql语句
        :return: 查询行JSON转成(处理数据库中的decimal、datetime、date类型)的字典
        """
        try:
            with self._db_conn.cursor() as cursor:
                self.__execute_sql(cursor, sqlStatement)
                allRows = cursor.fetchall()
                data = json.dumps(allRows, ensure_ascii=False, cls=CJsonEncoder)
                return json.loads(data)
        except Exception as e:
            raise e

    def execute_sql_string(self, sqlStatement):
        """
        mysql 增删改方法
        :param sqlStatement: sql语句
        :return: None
        """
        try:
            with self._db_conn.cursor() as cursor:
                self.__execute_sql(cursor, sqlStatement)
                self._db_conn.commit()
        except Exception as e:
            raise e

    def count_row(self, sqlStatement):
        """
        统计行数
        :param sqlStatement: sql语句
        :return: 行数
        """
        try:
            with self._db_conn.cursor() as cursor:
                self.__execute_sql(cursor, sqlStatement)
                cursor.fetchall()
                rowCount = cursor.rowcount
                return rowCount
        except Exception as e:
            print(e)
            raise e

    def __execute_sql(self, cur, sqlStatement):
        self._db_conn.ping(reconnect=True)
        print(sqlStatement)
        return cur.execute(sqlStatement)

    def close(self):
        """
        关闭连接
        :return: None
        """
        if self._db_conn:
            self._db_conn.close()

    def __del__(self):
        if self._db_conn:
            self._db_conn.close()


def sleep_db_query(func, sql, count=30, sleep=2):
    i = 1
    while i < count:
        res = func(sql)
        print('第{}次查询.........'.format(i))
        if res:
            print('查询结果 = {}.........'.format(res))
            return res
        i = i + 1
        time.sleep(sleep)


def wait_data_exist(func, sql, timeout=120):
    start_time = datetime.now()
    try:
        while 1:
            cur_time = datetime.now()
            if (cur_time - start_time).seconds >= timeout:
                raise Exception('waiting data sync: timeout')
            data = func(sql)
            if data:
                return data
            time.sleep(1)
    except Exception as e:
        raise e


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        elif isinstance(obj, date):
            return obj.__str__()
        # elif isinstance(obj, Decimal):
        #     return float(obj)
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


# To Generate string
def Dict2Str(dictin, joiner=','):
    # make dict to str, with the format key='value'
    # tmpstr=''
    tmplist = []
    for k, v in dictin.items():
        # if v is list, so, generate
        # "k in (v[0], v[1], ...)"
        if isinstance(v, (list, tuple)):
            tmp = str(k) + ' in (' + ','.join(map(lambda x: '\'' + str(x) + '\'', v)) + ') '
        else:
            if isinstance(v, str):
                tmp = str(k) + '=' + '\'' + str(v) + '\''
            else:
                tmp = str(k) + '=' + str(v)
        tmplist.append(' ' + tmp + ' ')
    return joiner.join(tmplist)


if __name__ == '__main__':
    db_conf = {
        'host': 'host',
        'db_name': 'db_name',
        'db_username': 'root',
        'db_password': 'root',
        'db_port': 3306
    }

    db = MysqlDb(db_conf)

    a = db.assemble_update('table', 'AND A = AAA', code='1111', sku=2222, sku2='sassasa', )
    #                       A=None, )
    # print(a)
    # db.close()
    # print(sleep_db_query(db.query, SQL))
