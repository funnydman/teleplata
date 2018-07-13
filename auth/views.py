import functools

from flask import Blueprint, request, session, flash, render_template, redirect, url_for, g

from .models import User

auth = Blueprint('auth', __name__,
                 url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user is None:
                error = 'Incorrect username.'
                flash(error, 'error')
            elif not user.check_password(password):
                error = 'Incorrect password.'
                flash(error, 'error')
            if error is None:
                session.clear()
                session['user_id'] = user.id
                flash('You were successfully logged in', 'success')
                return redirect(url_for('admin.admin'))

    return render_template("admin/login.html")


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))


@auth.before_app_request
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
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
