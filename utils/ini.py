# -*- coding: utf-8 -*-
# @Time    : 2020/1/22 9:51
# @Author  : weikai
# @File    : ini.py
# @Software: PyCharm
import configparser


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


@singleton
class ConfigIniParser(configparser.ConfigParser):
    def __init__(self, fileName):
        configparser.ConfigParser.__init__(self)
        self.fileName = fileName
        self.read(self.fileName, 'utf-8')

    def getAll(self, section):
        return dict(self.items(section))

    def getOne(self, section, option):
        return self.get(section, option)

    def setAll(self, section, confdic):
        for k, v in confdic.items():
            self.set(section, k, v)
        with open(self.fileName, "w+", encoding='utf-8') as cfile:
            self.write(cfile)

    def optionxform(self, optionstr):
        return optionstr


if __name__ == '__main__':
    a = ConfigIniParser('config.ini')
    print(a.getAll('app'))
    out = a.getAll('app')
    out['aaaa'] = '之后还会'
    a.setAll('app', out)
