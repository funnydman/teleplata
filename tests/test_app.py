def test_client(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'FUNNYDMAN' in rv.data
