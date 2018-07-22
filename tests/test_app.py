import random


def test_client(client):
    rv = client.get('/')
    assert rv.status_code == 200


def test_create_user(app):
    runner = app.test_cli_runner()
    random_string = ''.join(random.sample('abcdefgjinm', 5))
    result = runner.invoke(app.cli.commands['create_user'], ['--username', random_string, '--password', 'TETSTETS'])
    assert result.exit_code == 0


def test_get_pdf_report(app):
    runner = app.test_cli_runner()
    result = runner.invoke(app.cli.commands['get_pdf_report'])
    # TODO there is problem with travis
    # version `GLIBCXX_3.4.21' #not found wkhtmltopdf
    # assert result.exit_code == 0
