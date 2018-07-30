import os

import click
from flask import current_app
from flask.cli import with_appcontext

from teleplata.admin.models import User
from . import db


@click.command()
@click.option('--username', prompt=True, help='username')
@click.password_option()
@with_appcontext
def create_user(username, password):
    """Create super user."""
    if username and password:
        if not User.query.filter_by(username=username).first():
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            click.echo(f"User {username} created.")
        else:
            click.echo("User with this username exist.")
    else:
        click.echo("Enter username and password.")


@click.command()
@with_appcontext
def users():
    """Return all users"""
    user_list = User.query.all()
    if user_list:
        click.echo(user_list)
    else:
        click.echo("No users")


@click.command()
@with_appcontext
def get_pdf_report():
    """Make pdf report."""
    from .views import get_pdf_report
    report_folder = os.path.join(current_app.template_folder, 'report')
    get_pdf_report('report/report.html', report_folder)


@click.command()
@with_appcontext
def drop_db():
    """Drop database tables."""
    db.drop_all()
