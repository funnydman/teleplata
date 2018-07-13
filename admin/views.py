from flask import Blueprint, render_template, request

from auth.views import login_required
from main import TEMPLATE_FOLDER, STATIC_FOLDER
from main import db
from main.utils import get_class_by_tablename

bp_admin = Blueprint('admin', __name__,
                     url_prefix='/admin',
                     static_folder=STATIC_FOLDER,
                     template_folder=TEMPLATE_FOLDER)


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
        model = request.form['model']
        power = request.form['power']
        t_con = request.form['t_con']
        x_main = request.form['x_main']
        y_main = request.form['y_main']
        logic = request.form['logic']
        invertor = request.form['invertor']
        y_scan = request.form['y_scan']
        new_obj = brand(model=model, power=power, t_con=t_con, x_main=x_main,
                        y_main=y_main, logic=logic, invertor=invertor, y_scan=y_scan)
        if not brand.query.filter_by(model=model).first():
            db.session.add(new_obj)
            db.session.commit()
            is_sent_ok = True
        else:
            message = 'Такая модель уже есть в базе данных'
    last_five_models = brand.query.order_by(brand.pub_date.desc()).limit(5).all()
    return render_template('admin/models/model-add.html', brand=brand,
                           is_sent_ok=is_sent_ok, message=message, last_5_models=last_five_models)
