from __future__ import unicode_literals, absolute_import, division

from webtest import TestApp
from pytest import fixture
from mock import Mock


def pytest_cmdline_preparse(config, args):
    # TODO check that pytest-timeout is compatible with pytest-watch
    #args.append('--timeout=60')
    pass


@fixture(scope='function')
def _wsgi():
    # NOTE late import is required for monkey patching in tests
    from app import create_app
    return create_app()


@fixture(scope='function')
def client(_wsgi):
    return TestApp(_wsgi)


@fixture(scope='function')
def app(_wsgi):
    # TODO remove this workaround caused by wsgicors
    return _wsgi.application


@fixture(scope='function')
def uuid_mock(monkeypatch):
    uuid = Mock()
    uuid.return_value.hex = '11111111111111111111111111111111'
    monkeypatch.setattr('uuid.uuid4', uuid)


@fixture(scope='function')
def app_config():
    pass


@fixture(scope='function')
def http_mock():
    pass


@fixture(scope='function')
def time_mock():
    pass


@fixture(scope='function')
def simpleflake_mock():
    pass


@fixture(scope='function')
def token():
    pass


@fixture(scope='function')
def mailer_mock():
    pass


@fixture(scope='function')
def sentry_mock():
    pass