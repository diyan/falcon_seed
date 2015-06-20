from __future__ import unicode_literals, absolute_import, division

from falcon import HTTP_302, API as FalconApp
from wsgicors import CORS

from app.monitoring.handlers import StatusHandler, AppRoutesHandler
from app.common.falcon.error_handlers import setup_error_handlers


class IndexHandler:
    def on_get(self, req, res):
        res.status = HTTP_302
        res.location = '/api/v1/monitoring/status'


def setup_routes(app):
    """
    @type app: falcon.API
    """
    app.add_route('/', IndexHandler())
    app.add_route('/api/v1/monitoring/status', StatusHandler())
    app.add_route('/api/v1/monitoring/app_routes', AppRoutesHandler())


def setup_middleware(app):
    """
    @type app: falcon.API
    """
    # Falcon's OPTIONS responder does not follow CORS standard
    app = CORS(app, origin=b'*', headers=b'*', methods=b'*', credentials=b'true', maxage=b'1728000')
    return app


def create_app():
    app = FalconApp()
    setup_routes(app)
    setup_error_handlers(app)
    app = setup_middleware(app)
    return app
