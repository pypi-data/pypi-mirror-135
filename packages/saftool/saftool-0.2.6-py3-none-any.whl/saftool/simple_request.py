# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     simple_request
   Description :
   Author :        Asdil
   date：          2020/10/29
-------------------------------------------------
   Change Activity:
                   2020/10/29:
-------------------------------------------------
"""
__author__ = 'Asdil'
import json
import requests


def post(url, data, header=None):
    """post方法用于发送post
    Parameters
    ----------
    url : str
        url地址
    data : dict
        post body数据
    header : dict
        post header 数据
    Returns
    ----------
    """
    header = header if header else {'Content-Type': 'application/x-www-form-urlencoded'}
    ret = requests.post(url=url,
                        data=json.dumps(data),
                        headers=header)
    ret = ret.json()
    return ret


def get(url, headers={}, data={}):
    """get方法用于get数据
    Parameters
    ----------
    url : str
        url地址
    data : dict
        post data数据
    headers : dict
        post header 数据
    Returns
    ----------
    """
    response = requests.request("GET", url, headers=headers, data=data)
    return json.loads(response.text)