# -*- coding: utf-8 -*-
# @Time    : 2018/12/10 11:55
# @Author  : weikai
# @File    : Properties.py
# @Software: PyCharm
import traceback


class Properties(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.properties = {}

    def getProperties(self):
        pro_file = None
        try:
            # pro_file = open(self.fileName, mode='r')
            pro_file = open(self.fileName, mode='r', encoding='utf8', errors='ignore')
            for line in pro_file.readlines():
                line = line.strip().replace('\n', '')
                if line.find("#") != -1:
                    line = line[0:line.find('#')]
                if line.find('=') > 0:
                    strs = line.split('=')
                    strs[1] = line[len(strs[0]) + 1:]
                    self.properties[strs[0].replace(' ', '')] = strs[1].replace(' ', '')
        except Exception as e:
            print(traceback.format_exc())
            print(e)

        finally:
            if pro_file:
                pro_file.close()
        return self.properties
