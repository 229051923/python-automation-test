# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 14:26
# @Author  : weikai
# @File    : ftp.py
# @Software: PyCharm
import os
import ftplib


class FTP(object):
    ftp = ftplib.FTP()
    bIsDir = False
    path = ""

    def __init__(self, host, port, user, passwd):
        self.ftp.connect(host, port)
        self.ftp.login(user, passwd)
        print(self.ftp.welcome)

    def download_file(self, local_file, remote_file):
        file_handler = open(local_file, 'wb')
        self.ftp.retrbinary("RETR %s" % remote_file, file_handler.write)
        file_handler.close()
        return True

    def upload_file(self, local_file, remote_file):
        if not os.path.isfile(local_file):
            return False
        file_handler = open(local_file, "rb")
        self.ftp.storbinary('STOR %s' % remote_file, file_handler, 4096)
        file_handler.close()
        return True

    def upload_file_tree(self, local_dir, remote_file):
        if not os.path.isdir(local_dir):
            return False
        LocalNames = os.listdir(local_dir)
        self.ftp.cwd(remote_file)
        for Local in LocalNames:
            src = os.path.join(local_dir, Local)
            if os.path.isdir(src):
                self.upload_file_tree(src, Local)
            else:
                self.upload_file(src, Local)

        self.ftp.cwd("..")
        return

    def download_file_tree(self, local_dir, remote_dir):
        if not os.path.isdir(local_dir):
            os.makedirs(local_dir)
        self.ftp.cwd(remote_dir)
        r_names = self.ftp.nlst()
        for file in r_names:
            local = os.path.join(local_dir, file)
            if self.is_dir(file):
                self.download_file_tree(local, file)
            else:
                self.download_file(local, file)
        self.ftp.cwd("..")
        return

    def show(self, list):
        result = list.lower().split(" ")
        if self.path in result and "<dir>" in result:
            self.bIsDir = True

    def is_dir(self, path):
        self.bIsDir = False
        self.path = path
        # this ues callback function ,that will change bIsDir value
        self.ftp.retrlines('LIST', self.show)
        return self.bIsDir

    def close(self):
        self.ftp.close()

