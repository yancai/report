#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""
import os
from api.const import KEY_DOMAIN, PY_VERSION

if PY_VERSION == "3":
    from http import HTTPStatus as httplib
elif PY_VERSION == "2":
    import httplib as httplib

from flask import Blueprint, jsonify, request, current_app, send_file

from api.model import PersonalReport
from api.utils import list_report_by_date, verify_domain, get_md_path
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
        return jsonify({}), httplib.INTERNAL_SERVER_ERROR

    # 验证域账号
    if not verify_domain(user_id, d.get(KEY_DOMAIN, "")):
        return jsonify({"msg": "验证域账号失败"}), httplib.FORBIDDEN

    report = PersonalReport(
        date_str, user_id, d.get("yesterday", []), d.get("today", [])
    )
    try:
        report.save()
        return jsonify({"msg": "success"}), httplib.OK
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"msg": "error"}), httplib.INTERNAL_SERVER_ERROR


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


@api.route("/reports/md/<date_str>")
def get_daily_report_md(date_str):
    """获取Markdown格式日报

    :param date_str:
    :return:
    """

    # 是否以附件方式下载
    attachment = request.args.get("attachment", None) is not None

    mds = ["# 晨会纪要\n\n" + date_str + "\n"]

    files = list_report_by_date(date_str)
    for f in files:
        md = PersonalReport.load_from_file(f).to_md()
        mds.append(md)

    md_str = "\n------\n\n".join(mds)

    # 保存markdown文件
    md_path = os.path.realpath(os.path.join(
        get_md_path(date_str), date_str + ".md"
    ))
    with open(md_path, "w+") as f:
        f.write(md_str)

    return send_file(
        md_path,
        as_attachment=attachment,
        attachment_filename=date_str + ".md",
        mimetype="text/markdown"
    )


if __name__ == "__main__":
    pass
