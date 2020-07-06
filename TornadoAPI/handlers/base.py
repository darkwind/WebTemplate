from typing import Optional, Awaitable
from tornado.web import RequestHandler
import logging
import json
import random
import config


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)


class MainHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

    def initialize(self):
        self.rd = int(random.random() * 10000000000000000)
        logging.info("[HANDLER][%s] %s Start", self.rd, self.__class__.__name__)

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        # We capitalize the first letter of each component except the first one
        # with the 'title' method and join them together.
        return components[0] + ''.join(x.title() for x in components[1:])

    def rows_to_camel_case(self, rows):
        result = []
        for row in rows:
            item = {}
            for k, v in row.items():
                item[self.to_camel_case(k)] = v
            result.append(item)
        return result

    def row_to_camel_case(self, row):
        item = {}
        for k, v in row.items():
            item[self.to_camel_case(k)] = v
        return item

    def log_query(self, query):
      pass

    def success(self, data):
        self.write(
            json.dumps(
                {"code": 200, "data": data},
                ensure_ascii=False,
                cls=DatetimeEncoder  # 한글 인코딩 문제 처리
            )
        )

    def fail(self, data):
        self.write(
            json.dumps(
                {"code": 500, "data": data},
                ensure_ascii=False,
                cls=DatetimeEncoder,
            )
        )

    def text(self, data):
        self.write(data)

    def on_finish(self):
        logging.info("[HANDLER][%s] %s Finish", self.rd, self.__class__.__name__)
