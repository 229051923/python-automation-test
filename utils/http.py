# -*- coding: utf-8 -*-
# @Time    : 2020/1/22 9:45
# @Author  : weikai
# @File    : http.py
# @Software: PyCharm
import os
import re
from urllib import parse
import requests
import json as _json
import logging as logger


class ApiRequest(object):
    """
    http请求
    """

    def __init__(self):
        self.session = requests.session()

    def post(self, url, data=None, json=None, **kwargs):
        logger.info(f'请求URL=[{url}]')
        if data:
            if isinstance(data, bytes):
                logger.info(f"请求消息体=[{bytes.decode(data, 'utf-8')}]")
            else:
                logger.info(f"请求消息体=[{data}]")
        if json:
            logger.info(f"请求消息体=[{_json.dumps(json, ensure_ascii=False)}]")
        logger.info(f'其他参数=[{kwargs}]')
        response = self.session.post(url, data=data, json=json, **kwargs)
        if len(response.text) >= 1024 * 5:
            logger.info(f"返回消息体=[{response.text[0:1024 * 5]}] ...")
        else:
            logger.info(f"返回消息体=[{response.text}]")
        logger.info(f"返回状态码=[{response.status_code}]")
        logger.info(f"请求响应时间=[{response.elapsed.total_seconds()}]秒")
        assert response.status_code == 200
        return response

    def get(self, url, params=None, is_remove_empty=False, **kwargs):
        logger.info(f'请求URL=[{url}]')
        if params:
            logger.info(f"请求参数=[{params}]")
            # 接口不统一，参数为空和不到字段部分接口存在区别
            if is_remove_empty:
                params = _remove_empty_values(params)
        logger.info(f'其他参数=[{kwargs}]')

        response = self.session.get(url, params=params, **kwargs)
        if len(response.text) >= 1024 * 5:
            logger.info(f"返回消息体=[{response.text[0:1024 * 5]}] ...")
        else:
            logger.info(f"返回消息体=[{response.text}]")
        logger.info(f"返回状态码=[{response.status_code}]")
        logger.info(f"请求响应时间=[{response.elapsed.total_seconds()}]秒")
        assert response.status_code == 200
        return response

    def get_file(self, url, params=None, is_remove_empty=False, **kwargs):
        logger.info(f'请求URL=[{url}]')
        if params:
            logger.info(f"请求参数=[{params}]")
            # 接口不统一，参数为空和不到字段部分接口存在区别
            if is_remove_empty:
                params = _remove_empty_values(params)
        response = self.get(url, stream=True, params=params, **kwargs)
        file = response.headers.get("Content-Disposition")
        filename = re.findall('filename=(.*)', file)
        filename = filename[0]
        # 如果是中文需要解码
        filename = parse.unquote(filename)
        # 默认存储在easytest_log 日志路径
        filename = os.path.join(get_log_dir(), filename)
        logger.info(f"文件路径{filename}")
        if os.path.exists(filename):
            os.remove(filename)
            logger.info("文件已存在，删除文件")
        with open(filename, "wb") as code:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    code.write(chunk)
        return filename


def _remove_empty_values(data: dict) -> dict:
    for k in list(data.keys()):
        if not data[k] and data[k] != 0:
            del data[k]
    return data
