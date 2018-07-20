import os


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

def test_get_pdf_report(app):
    runner = app.test_cli_runner()
    runner.invoke(app.cli.commands['get_pdf_report'])
    path_to_report_file = os.path.join(app.template_folder, 'report', 'report.pdf')
    assert os.path.exists(path_to_report_file)
