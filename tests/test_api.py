import json

testobj = {'message_content': 'test message',
           'delivery_time': '2020-08-13T06:00:00'}


def test_api_get_statuscode(app, client):
    res = client.get('/api/get/scheduler1')
    assert res.status_code == 202


def test_api_get_statuscode_404(app, client):
    res = client.get('/api/get/unknown9123')
    assert res.status_code == 404


def test_api_get_resp_404(app, client):
    res = client.get('/api/get/unknown9123')
    assert "doesn't exist" in json.loads(
        res.get_data(as_text=False))["message"]


def test_api_get_resp(app, client):
    res = client.get('/api/get/scheduler1')
    assert "message_content" in json.loads(res.get_data(as_text=False))[0]


def test_api_alljobs_statuscode(app, client):
    res = client.get('/api/alljobs')
    assert res.status_code == 202


def test_api_alljobs_statuscode_404(app, client):
    res = client.get('/api/alljobs1')
    assert res.status_code == 404


def test_api_addjob_statuscode(app, client):
    res = client.post('/api/addjob', json=testobj)
    assert res.status_code == 202


def test_api_addjob_statuscode_500(app, client):
    res = client.post('/api/addjob', json={})
    assert res.status_code == 500


def test_api_addjob(app, client):
    res = client.post('/api/addjob', json=testobj)
    assert True == json.loads(res.get_data(as_text=False))['Accepted']


def test_api_deljob_statuscode(app, client):
    res = client.get('/api/alljobs')
    last_id = json.loads(res.get_data(as_text=False))[-1]['scheduler_id']
    r = client.delete('api/delete/'+last_id)
    assert r.status_code == 202


def test_api_deljob_resp(app, client):
    res = client.get('/api/alljobs')
    last_id = json.loads(res.get_data(as_text=False))[-1]['scheduler_id']
    r = client.delete('api/delete/'+last_id)
    assert True == json.loads(r.get_data(as_text=False))['Accepted']
