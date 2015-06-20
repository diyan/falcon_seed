from __future__ import unicode_literals, absolute_import, division


def test_status(client):
    res = client.get('/api/v1/monitoring/status')
    assert res.json['result']['status'] == 'OK'
    # TODO assert full json body