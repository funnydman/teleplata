import os
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
    runner.invoke(app.cli.commands['get_pdf_report'])
    path_to_report_file = os.path.join(app.template_folder, 'report', 'report.pdf')
    assert os.path.exists(path_to_report_file)
