# -*- coding: utf-8 -*-
# @Time    : 2019/8/2 10:21
# @Author  : weikai
# @File    : dict2obj.py
# @Software: PyCharm
# 字典转对象
class DictTObj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [DictTObj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, DictTObj(b) if isinstance(b, dict) else b)
