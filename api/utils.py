#!/usr/bin/python
# -*- coding:utf-8 -*-
from datetime import date, timedelta
import os
from os import path

from flask import current_app

from api.const import KEY_DOMAIN
from settings import USERS, DATA_DIR

_user_map = {}


def get_user_map():
    """获取user_map

    :return:
    """
    global _user_map
    if _user_map == {}:
        _user_map = {
            i["id"]: {"name": i["name"], KEY_DOMAIN: i[KEY_DOMAIN]}
            for i in USERS
        }
    return _user_map


def get_date(delta=0):
    """获取日期字符串

    :param delta: 与当前日期天数差，-1代表昨天，-2代表前天，1代表明天
    :return:
    """
    today = date.today()
    tdelta = timedelta(days=delta)
    target_date = today + tdelta
    date_str = target_date.strftime("%Y-%m-%d")
    return date_str


def prepare_path(filepath):
    """准备指定文件夹文件夹

    :param filepath:
    :return:
    """
    if not path.exists(filepath):
        os.makedirs(filepath)


def list_report_by_date(date_str):
    """获取指定日期的日报

    :param date_str:
    :return:
    """
    report_dir = path.realpath(path.join(
        current_app.root_path, DATA_DIR, "json", date_str,
    ))

    filenames = os.listdir(report_dir)
    files = [path.join(report_dir, f) for f in filenames]

    return files


def verify_domain(user_id, domain):
    """验证用户对应的域账号是否正确

    :param user_id:
    :param domain:
    :return:
    """
    user_map = get_user_map()
    return user_map.get(user_id, {}).get(KEY_DOMAIN, None) == domain


def get_md_path(date_str):
    """获取Markdown文件存储位置

    :param date_str:
    :return:
    """
    md_dir = path.realpath(path.join(
        current_app.root_path, DATA_DIR, "md", date_str
    ))
    prepare_path(md_dir)
    return md_dir


if __name__ == "__main__":
    pass
