# -*- coding: utf-8 -*-

"""
/*
*
* Auther： Wenjie Zheng <wjzheng@robosense.cn>
* File:    globlvar8.py 
*
*/
"""

import robosense.general as gen

def __init():
    global _local_dict
    try:
        _local_dict()
    except NameError:
        _local_dict = {}
        return True
    except TypeError:
        return True
    else:
        return False

def set(name, value):
    __init()
    _local_dict[name] = value


def get(name, defvalue=None):
    __init()
    try:
        return _local_dict[name]

    except KeyError:
        return defvalue


def update(inputdict):
    __init()
    # 将某个字典的键/值对更新到全局变量字典
    if isinstance(inputdict, dict) == True:
        _local_dict.update(inputdict)


def overlay(inputdict):
    __init()
    # 将某个字典导入全局变量字典
    if isinstance(inputdict, dict) == True:
        # 先清空_global_dict
        c = {}
        _local_dict.update(c)

        # 再覆盖_global_dict
        c.update(inputdict)
        _local_dict.update(c)


def showall():
    __init()
    gen.TYPE(_local_dict)


def show(name):
    __init()
    gen.TYPE(_local_dict[name])


def lenall():
    __init()
    # gen.TYPE(len(_local_dict))
    return len(_local_dict)


def lenkey(name):
    __init()
    # gen.TYPE(len(_local_dict[name]))
    return len(_local_dict[name])
