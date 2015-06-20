from __future__ import unicode_literals, absolute_import, division

from pytest import fixture

from tests.assertions import assert_deep_equal


class ErrorHandler:
    def on_post(self, req, res):
        res.body = 1 / 0


class HelloHandler:
    def on_get(self, req, res):
        res.body = 'Hello'

    def on_post(self, req, res):
        res.body = 'Hello'


@fixture(scope='function')
def client(uuid_mock, app, client):
    app.add_route('/testing/error', ErrorHandler())
    app.add_route('/testing/hello', HelloHandler())
    return client


def test_preflight_request_should_return_cors_headers(client):
    # TODO update webtest client, let developer pass HTTP header value as unicode string
    res = client.options('/testing/hello', headers={
        'Origin': b'http://example.com',
        'Access-Control-Request-Method': b'POST',
        'Access-Control-Request-Headers': b'Accept, Content-Type, Authorization'
    })

    assert res.status_code == 204, res.text
    cors_headers = dict((k, v) for k, v in res.headers.items() if 'Access-Control' in k)
    assert_deep_equal(cors_headers, {
        'Access-Control-Allow-Headers': 'Accept, Content-Type, Authorization',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Max-Age': '1728000'
    })


def test_post_should_return_cors_headers(client):
    res = client.post('/testing/hello', headers={'Origin': b'http://example.com'})

    assert res.status_code == 200, res.text
    assert res.text == 'Hello'
    cors_headers = dict((k, v) for k, v in res.headers.items() if 'Access-Control' in k)
    assert_deep_equal(cors_headers, {
        'Access-Control-Allow-Origin': 'http://example.com',
        'Access-Control-Allow-Credentials': 'true'
    })


def test_get_error_should_return_cors_headers(client):
    res = client.post('/testing/error', headers={'Origin': b'http://example.com'}, expect_errors=True)

    assert res.status_code == 500, res.text
    assert_deep_equal(res.json, {
        'error': {
            'id': '11111111111111111111111111111111',
            'type': 'internal',
            'message': 'division by zero'
        }
    })
    cors_headers = dict((k, v) for k, v in res.headers.items() if 'Access-Control' in k)
    assert_deep_equal(cors_headers, {
        'Access-Control-Allow-Origin': 'http://example.com',
        'Access-Control-Allow-Credentials': 'true'
    })