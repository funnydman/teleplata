def test_client(client):
    rv = client.get('/')
    assert rv.status_code == 200

# TODO can't test it cause test_config fails. But why?
# def test_create_user(app):
#     runner = app.test_cli_runner()
#
#     # invoke the command directly
#     result = runner.invoke(app.cli.commands['create_user'], ['--username', 'TEST', '--password', 'TETSTETS'])
#     assert 'User created' in result.output
