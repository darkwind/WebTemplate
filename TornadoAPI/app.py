#!/usr/bin/env python3
# coding=utf-8
from tornado import ioloop
# from tornado.web import StaticFileHandler
from tornado.web import RedirectHandler
from tornado.options import options, parse_command_line
from tornado.httpserver import HTTPServer

import tornado_swirl as swirl
import logging
import datetime
import os

import config


# todo: logs 디렉토리가 있는지 확인하고 없으면 생성
path_logs = os.path.join(os.getcwd(),"logs")
if not os.path.exists(path_logs):
    os.makedirs(path_logs)

# 로그 설정
dt = datetime.datetime.now()
options.logging = 'info'
options.log_to_stderr = True
options.log_file_prefix = './logs/app_%s.log' % dt.strftime("%Y%m%d")
options.log_file_max_size = (100 * 1000 * 1000)
options.log_file_num_backups = 10
options.log_rotate_when = 'midnight'
options.log_rotate_interval = 1
options.log_rotate_mode = 'time'
parse_command_line()

def make_app():
    logging.info("Server start http://%s:%i", config.app_host, config.app_port)
    logging.info("DOC start http://%s:%i/docs/spec.html", config.app_host, config.app_port)
    settings = dict(
        cookie_secret=config.app_key,
        debug=True,
        description=config.app_title,
    )

    # 라우트 설정
    routes = swirl.api_routes() + [
        (r"/(.*)", RedirectHandler, {'url': '/api'}),
    ]
    return swirl.Application(routes, **settings)


if __name__ == "__main__":
    app = make_app()
    server = HTTPServer(app)
    server.bind(config.app_port)
    server.start(1)  # Forks multiple sub-processes
    ioloop.IOLoop.current().start()
