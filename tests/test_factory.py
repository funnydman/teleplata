def test_testing_config(app):
    assert app.config['DEBUG']
    assert app.config['TESTING']
