# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     wrap
   Description :
   Author :       asdil
   date：          2022/1/17
-------------------------------------------------
   Change Activity:
                   2022/1/17:
-------------------------------------------------
"""
__author__ = 'Asdil'
from datetime import datetime
import time


def type_assert(*ty_args, **ty_kwargs):
    """type_assert方法用于强制确认输入格式

    @type_assert(int, b=str)
    f(a, b)

    Parameters
    ----------
    Returns
    ----------
    """
    from inspect import signature
    from functools import wraps

    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(
                                name, bound_types[name]))
            return func(*args, **kwargs)
        return wrapper
    return decorate


def runtime(func):
    """
    运行时间的装饰器
    :param : python function
    :return:
    """
    def wrapper(*args, **kwargs):
        start_now = datetime.now()
        start_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        end_now = datetime.now()
        print(f'time时间:{end_time-start_time}\ndatetime起始时间:{start_now} 结束时间:{end_now}, 一共用时{end_now-start_now}')
        return ret
    return wrapper

