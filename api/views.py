#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Documentation"""

from flask import Blueprint, jsonify, request, redirect, url_for, current_app

from settings import USERS

api = Blueprint(
    "index", __name__
)


@api.route("/users/")
def get_all_user():
    return jsonify({"users": USERS})
    pass


if __name__ == "__main__":
    pass
