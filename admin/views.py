from flask import Blueprint, render_template, request, flash

from auth.views import login_required
from main import db, TEMPLATE_FOLDER, STATIC_FOLDER
from main.utils import get_class_by_tablename

bp_admin = Blueprint('admin', __name__,
                     url_prefix='/admin',
                     static_folder=STATIC_FOLDER,
                     template_folder=TEMPLATE_FOLDER)


@bp_admin.route('/')
@login_required
def admin():
    return render_template('admin/admin.html')


def get_form_data(request):
    result_dict = {}
    table_fields = ('model', 'power', 't_con', 'x_main',
                    'y_main', 'logic', 'invertor', 'y_scan')
    for field in table_fields:
        result_dict.update({field: request.form[field]})
    return result_dict


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
