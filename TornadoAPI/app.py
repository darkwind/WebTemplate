#!/usr/bin/env python3
# coding=utf-8

from tornado import ioloop
from tornado import netutil, process

# from tornado.web import StaticFileHandler
from tornado.web import RedirectHandler
from tornado.options import options, parse_command_line
from tornado.httpserver import HTTPServer

import tornado_swirl as swirl
import logging
import datetime
import os
import sys, asyncio

import config
import scheme


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
    logging.info("DOC start http://%s:%i/swagger/spec.html", config.app_host, config.app_port)
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
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = make_app()

    # For Single Process
    server = HTTPServer(app)
    app.listen(config.app_port)
    ioloop.IOLoop.current().start()

    # # For Multi Process
    # sockets = netutil.bind_sockets(config.app_port)
    # process.fork_processes(0)
    # server HTTPServer(app)
    # server.add_sockets(sockets)
    # ioloop.IOLoop.current().start()