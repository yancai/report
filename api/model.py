#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
from os import path

from flask import current_app

from api.const import KEY_USER_ID, KEY_USER_NAME, KEY_DATE_STR, KEY_YESTERDAY, KEY_TODAY
from api.utils import get_user_map, get_date, prepare_path
from settings import DATA_DIR


class PersonalReport(object):
    """个人晨报
    """

    date_str = ""
    user_id = ""
    yesterday = []
    today = []

    user_map = get_user_map()

    def __init__(self, date_str, user_id, yesterday, today):
        """初始化个人晨报

        :param date_str: 日期字符串
        :param user_id: 用户id
        :type yesterday: list
        :param yesterday: 昨日已完成任务
        :type today: list
        :param today: 今天计划任务
        """
        self.date_str = date_str
        self.user_id = user_id
        self.user_name = self.user_map.get(self.user_id)
        self.yesterday = yesterday
        self.today = today

    def to_map(self):
        return {
            KEY_USER_ID: self.user_id,
            KEY_USER_NAME: self.user_name,
            KEY_DATE_STR: self.date_str,
            KEY_YESTERDAY: self.yesterday,
            KEY_TODAY: self.today,
        }

    def save(self):
        """保存晨报到文件

        :return:
        """
        filename = path.realpath(path.join(
            current_app.root_path, DATA_DIR, self.date_str,
            u"{}-{}.json".format(self.user_id, self.user_name)
        ))

        prepare_path(path.dirname(filename))

        with open(filename, "w+", encoding="utf-8") as f:
            json.dump(self.to_map(), f)

    @staticmethod
    def load_from_file(filepath):
        """从文件生成个人日报

        :param filepath:
        :return:
        :rtype: PersonalReport
        """
        with open(filepath, "r+") as f:
            data = json.load(f)
            return PersonalReport(
                data.get(KEY_DATE_STR, ""),
                data.get(KEY_USER_ID, ""),
                data.get(KEY_YESTERDAY, []),
                data.get(KEY_TODAY, [])
            )


class DailyReport(object):
    """晨报
    """

    date_str = ""
    yesterday = []
    today = []

    def __init__(self, yesterday, today, date_str=None):
        """初始化晨报

        :param yesterday:
        :param today:
        :param date_str:
        """
        self.yesterday = yesterday
        self.today = today
        self.date_str = get_date() if date_str is None else date_str


if __name__ == "__main__":
    pass
