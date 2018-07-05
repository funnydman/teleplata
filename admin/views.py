from flask import Blueprint, render_template, request

from main import TEMPLATE_FOLDER, STATIC_FOLDER

bp_admin = Blueprint('admin', __name__,
                     url_prefix='/admin',
                     static_folder=STATIC_FOLDER,
                     template_folder=TEMPLATE_FOLDER)


@bp_admin.route('/')
def admin():
    return render_template('admin/admin.html')


@bp_admin.route('/<brand>')
def show_models_by_brand(brand):
    from main.utils import get_class_by_tablename
    page = request.args.get('page', 1)
    models = get_class_by_tablename(brand).query.paginate(page=int(page),
                                                          per_page=2,
                                                          error_out=False)
    return render_template('admin/models/model-list.html', models=models)
