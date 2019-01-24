#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""
from http import HTTPStatus

from flask import Blueprint, jsonify, request, current_app

from api.const import KEY_DOMAIN
from api.model import PersonalReport
from api.utils import list_report_by_date, verify_domain
from settings import USERS

api = Blueprint(
    "index", __name__
)


@api.route("/users/")
def get_all_user():
    """获取全部用户列表

    :return:
    """
    return jsonify({"users": USERS})


@api.route("/report/<date_str>/<user_id>/", methods=["PUT"])
def create_daily_report(date_str, user_id):
    """创建日报

    :param date_str:
    :param user_id:
    :return:
    """

    try:
        d = request.get_json()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({}), HTTPStatus.INTERNAL_SERVER_ERROR

    # 验证域账号
    if not verify_domain(user_id, d.get(KEY_DOMAIN, "")):
        return jsonify({"msg": "验证域账号失败"}), HTTPStatus.FORBIDDEN

    report = PersonalReport(
        date_str, user_id, d.get("yesterday", []), d.get("today", [])
    )
    try:
        report.save()
        return jsonify({"msg": "success"}), HTTPStatus.OK
    except Exception as e:
        current_app.logger.errror(e)
        return jsonify({"msg": "error"}), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/reports/<date_str>/")
def get_reports(date_str):
    """获取某日所有日报

    :param date_str:
    :return:
    """

    files = list_report_by_date(date_str)

    reports = []
    for f in files:
        report = PersonalReport.load_from_file(f).to_map()
        reports.append(report)

    return jsonify({"data": reports})


if __name__ == "__main__":
    pass
