import functools

from flask import Blueprint, render_template, request, flash, session, url_for, redirect, g

from teleplata.admin.models import User
from teleplata.main import db, TEMPLATE_FOLDER, STATIC_FOLDER
from teleplata.main.utils import get_class_by_tablename
from .utils import get_form_data

bp_admin = Blueprint('admin', __name__,
                     url_prefix='/admin',
                     static_folder=STATIC_FOLDER,
                     template_folder=TEMPLATE_FOLDER)


@bp_admin.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('admin.admin'))

    return render_template("admin/login.html")


@bp_admin.route('/logout')
def logout():
    session.clear()
    flash('You were logged out', 'success')
    return redirect(url_for('main.home'))


@bp_admin.before_app_request
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
            return redirect(url_for('admin.login'))
        return view(**kwargs)

    return wrapped_view


@bp_admin.route('/')
@login_required
def admin():
    return render_template('admin/admin.html')


@bp_admin.route('/<brand>', methods=['GET', 'POST'])
@login_required
def add_new_model(brand):
    is_sent_ok = False
    message = None
    brand = get_class_by_tablename(brand)
    if request.method == 'POST':
        form_data = get_form_data(request)
        new_model_obj = brand(model=form_data['model'],
                              power=form_data['power'],
                              t_con=form_data['t_con'],
                              x_main=form_data['x_main'],
                              y_main=form_data['y_main'],
                              logic=form_data['logic'],
                              invertor=form_data['invertor'],
                              y_scan=form_data['y_scan'])
        if not brand.query.filter_by(model=form_data['model']).first():
            db.session.add(new_model_obj)
            db.session.commit()
            is_sent_ok = True
        else:
            message = 'Такая модель уже есть в базе данных'
            flash(message)
    last_five_models = brand.query.order_by(brand.pub_date.desc()).limit(5).all()
    return render_template('admin/models/model-add.html', brand=brand,
                           is_sent_ok=is_sent_ok, message=message, last_five_models=last_five_models)


@bp_admin.route('/edit/<brand>/<model>', methods=['GET', 'POST'])
@login_required
def model_edit(brand, model):
    brand = get_class_by_tablename(brand)
    model_to_edit = brand.query.filter_by(model=model)
    if request.method == 'POST':
        # TODO add method to add data
        model_edited = model_to_edit.update()
        print(model_edited)
        db.session.commit()
        return
    return render_template("admin/models/model-edit.html", model_to_edit=model_to_edit.first())
