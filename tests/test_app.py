def test_client(client):
    rv = client.get('/')
    assert rv.status_code == 200
