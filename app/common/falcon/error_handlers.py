from __future__ import unicode_literals, absolute_import, division
import re
import json
from uuid import uuid4

import falcon.responders
from falcon import HTTP_500, HTTP_404, HTTP_405

from app.common.errors import BaseAppError
from app.common.text_utils import to_first_lower


def _handle_app_error(ex, req, res, params):
    # TODO send error to sentry
    # TODO display error stack if X-Debug were specified
    res.status = HTTP_500
    res.body = json.dumps(dict(error=dict(
        id=uuid4().hex,
        message=ex.message,
        type=re.sub('Error$', '', to_first_lower(type(ex).__name__))
    )))


def _handle_internal_error(ex, req, res, params):
    # TODO send error to sentry
    # TODO display error stack if X-Debug were specified
    res.status = HTTP_500
    res.body = json.dumps(dict(error=dict(
        id=uuid4().hex,
        message=ex.message,
        type='internal'  # NOTE do not expose real type of unhandled error
    )))


def _not_found_responder(req, res, **kwargs):
    # TODO send error to sentry
    res.status = HTTP_404
    res.body = json.dumps(dict(error=dict(
        id=uuid4().hex,
        message='Requested resource is not found',
        type='notFound'
    )))


def _create_method_not_allowed_responder(allowed_methods):
    allowed = ', '.join(allowed_methods)

    def method_not_allowed(req, res, **kwargs):
        res.status = HTTP_405
        res.set_header('Allow', allowed)
        res.body = json.dumps(dict(error=dict(
            id=uuid4().hex,
            message='The method is not allowed for the requested resource',
            type='methodNotAllowed',
            allowed_methods=allowed_methods
        )))

    return method_not_allowed


def _patch_responders():
    # There are no way to override Falcon responders other than monkey patching
    falcon.responders.path_not_found = _not_found_responder
    falcon.responders.create_method_not_allowed \
        = _create_method_not_allowed_responder
    # TODO consider also patch default bad_request responder


def setup_error_handlers(app):
    """
    @type app: falcon.API
    """
    _patch_responders()
    app.add_error_handler(BaseAppError, _handle_app_error)
    app.add_error_handler(Exception, _handle_internal_error)
