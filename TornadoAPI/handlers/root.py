# coding=utf-8
import tornado_swirl as swirl
from handlers.base import MainHandler


@swirl.restapi('/api')
class RootHandler(MainHandler):

    def get(self):
        """사이트 메인

        Tags:
            Common
        DEPRECATED
        """
        self.success({
            "title": "API Root",
        })
