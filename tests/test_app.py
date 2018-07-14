def test_client(client):
    rv = client.get('/')
    assert b'FUNNYDMAN' in rv.data
