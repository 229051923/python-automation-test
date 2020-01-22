# -*- coding: utf-8 -*-
# @Time    : 2020/1/2 16:08
# @Author  : weikai
# @File    : jinja_sql_util.py
# @Software: PyCharm
from six import string_types
from copy import deepcopy
from jinjasql import JinjaSql


def apply_sql_template(template, parameters):
    """
    根据模板返回sql ,如果使用like语句 使用CONCAT({{ user_id }} ,"%%")拼接
    :param template: 模板字符串
    :param parameters:入参
    :return:
    """
    j = JinjaSql(param_style='pyformat')
    query, bind_params = j.prepare_query(template, parameters)
    return _get_sql_from_template(query, bind_params)


def _quote_sql_string(value):
    """
    format增加单引号
    :param value:
    :return:
    """
    if isinstance(value, string_types):
        new_value = str(value)
        new_value = new_value.replace("'", "''")
        return "'{}'".format(new_value)
    return value


def _get_sql_from_template(query, bind_params):
    """
    :param query:
    :param bind_params:
    :return:
    """
    if not bind_params:
        return query
    params = deepcopy(bind_params)
    for key, val in params.items():
        params[key] = _quote_sql_string(val)
    return query % params


if __name__ == '__main__':
    template = """
        SELECT project, timesheet, hours
        FROM timesheet
        {% if user_id and t=="1" %}
        WHERE user_id like  CONCAT({{ user_id }} ,"%%")
         {% endif %}
        {% if project_id %}
        AND project_id = {{ project_id }}
        {% endif %}
        AND TEST IN {{ days| inclause }}
    """
    tmep2="""
    """
    data = {
        "t":"2",
        "project_id": "2",
        "user_id": "sripathi",
        "days": ["1a", "2"]
    }
    print(apply_sql_template(template, data))
