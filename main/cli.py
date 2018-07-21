import click
from flask.cli import with_appcontext

from main import db


@click.command()
@click.option('--username', prompt=True, help='username')
@click.password_option()
@with_appcontext
def create_user(username, password):
    """Create super user."""
    if username and password:
        from auth.models import User
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        # click.echo(f'User {username} created')
    else:
        click.echo("Enter username and password")


@click.command()
@with_appcontext
def get_pdf_report():
    """Make pdf report."""
    from .views import get_pdf_report
    get_pdf_report()
