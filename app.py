#!/usr/bin/python
# -*- coding:utf-8 -*-


from flask import Flask, render_template

from api.views import api

app = Flask(__name__)

@app.route("/favicon.ico")
def get_favicon():
    """favicon.ico
    """
    return app.send_static_file("favicon.ico")

@app.route("/")
def page_index():
    """页面-首页
    """
    return render_template("index.html")


@app.route("/report")
def page_daily_report():
    """页面-每日晨报

    :return:
    """
    return render_template("daily_report.html")


# 注册api接口的blueprint
app.register_blueprint(api, url_prefix="/api")


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
    pass
