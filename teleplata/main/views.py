import functools
import os

from flask import Blueprint, render_template, request, send_from_directory, flash, session, redirect, g, url_for
from flask import current_app

from teleplata.admin.models import User
from . import db
from .utils import get_class_by_tablename, get_pdf_report, paginate

main = Blueprint('main', __name__)


@main.route('/report/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    report_folder = os.path.join(current_app.template_folder, 'report')
    filename = get_pdf_report('report/report.html', report_folder)
    return send_from_directory(directory=report_folder, filename=filename)


@main.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user is None:
                error = 'Incorrect username or user does not exist'
                flash(error, 'error')
            elif not user.check_password(password):
                error = 'Incorrect password.'
                flash(error, 'error')
            if error is None:
                session.clear()
                session['user_id'] = user.id
                flash('You were logged in', 'success')
                return redirect('/')
    return render_template('home/login.html')


@main.route('/logout')
def logout():
    session.clear()
    flash('You were logged out', 'success')
    return redirect(url_for('main.home'))


@main.route('/', methods=['GET', 'POST'])
@main.route('/<brand>/', methods=['POST', 'GET'])
def home(brand='samsung'):
    brand = get_class_by_tablename(brand)
    page = request.args.get('page', 1, type=int)
    models = paginate(brand.query, page)
    return render_template('home/home.html', models=models, brand=brand)


@main.before_app_first_request
def setup_application():
    db.create_all()


@main.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('main.login'))
        return view(**kwargs)

    return wrapped_view
