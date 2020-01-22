# -*- coding: utf-8 -*-
# @Time    : 2018/12/3 9:30
# @Author  : weikai
# @File    : time_tools.py
# @Software: PyCharm
import time
import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


# 获取当前时间格式化
def get_now_time(time_format=DATETIME_FORMAT):
    return datetime.datetime.strftime(datetime.datetime.now(), time_format)


# 几天前的时间/几天后 days 可以为正负数
def get_add_days(days, time_format=DATE_FORMAT):
    daysAgoTime = datetime.datetime.now() - datetime.timedelta(days=days)
    return time.strftime(time_format, daysAgoTime.timetuple())


# 当前毫秒数
def get_cur_milis():
    return int(time.time() * 1000)


# 当前秒数
def get_cur_seconds():
    return int(time.time())


# 当前年
def get_cur_year():
    return datetime.datetime.now().year


# 当前月
def get_cur_month():
    return datetime.datetime.now().month


# 当前日
def get_cur_day():
    return datetime.datetime.now().day


# 当前时
def get_cur_hour():
    return datetime.datetime.now().hour


# 当前分
def get_cur_minute():
    return datetime.datetime.now().minute


# 当前秒
def get_cur_second():
    return datetime.datetime.now().second


# 星期几
def get_cur_week():
    return datetime.datetime.now().weekday()


if __name__ == '__main__':
    print(get_add_days(-2))
