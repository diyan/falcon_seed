from __future__ import unicode_literals, absolute_import, division
import json

from structlog import get_logger


class StatusHandler:
    def __init__(self):
        self.logger = get_logger()

    def on_get(self, req, res):
        """
        @type req: falcon.request.Request
        @type res: falcon.response.Response
        """
        rv = dict(
            status='OK',
            settings={},  # TODO pass some/all settings here
            content_type=req.content_type,
            url=req.url,
            remote_addr='',  # TODO Use falcon or wgsi API to get remote addr
            headers=req.headers,
            cookies=req.cookies,
            context=req.context)
        res.body = json.dumps(dict(result=rv))


class AppRoutesHandler:
    def __init__(self):
        self.logger = get_logger()

    def on_get(self, req, res):
        # TODO return result: routes?: [handler, url, methods]
        pass