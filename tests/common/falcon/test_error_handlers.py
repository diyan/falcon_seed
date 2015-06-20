from __future__ import unicode_literals, absolute_import, division

from pytest import fixture

from tests.assertions import assert_deep_equal


class InternalErrorHandler:
    def on_get(self, req, res):
        res.body = 1 / 0


@fixture(scope='function')
def client(uuid_mock, app, client):
    app.add_route('/testing/error', InternalErrorHandler())
    return client


def test_internal_error(client):
    # TODO test error traceback visible/hidden depending on X-Debug header
    res = client.get('/testing/error', expect_errors=True)
    assert res.status_code == 500, res.text
    assert_deep_equal(res.json, {
        'error': {
            'id': '11111111111111111111111111111111',
            'type': 'internal',
            'message': 'division by zero'
        }
    })


def test_app_error(client):
    # TODO
    pass


def test_not_found(client):
    res = client.delete_json('/testing/not_existed', expect_errors=True)

    assert res.status_code == 404, res.text
    assert_deep_equal(res.json, {
        'error': {
            'id': '11111111111111111111111111111111',
            'type': 'notFound',
            'message': 'Requested resource is not found'
        }
    })


def test_method_not_allowed(client):
    res = client.delete('/testing/error', expect_errors=True)

    assert res.status_code == 405, res.text
    assert_deep_equal(res.json, {
        'error': {
            'id': '11111111111111111111111111111111',
            'type': 'methodNotAllowed',
            'message': 'The method is not allowed for the requested resource',
            'allowed_methods': ['OPTIONS', 'GET']
        }
    })