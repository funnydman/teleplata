import os

from flask import Blueprint, render_template, request, g, send_from_directory
from flask import current_app

from . import db
from .utils import get_class_by_tablename, get_pdf_report, paginate

main = Blueprint('main', __name__)


@main.route('/report/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    filename = get_pdf_report()
    path_to_file = os.path.join(current_app.template_folder, 'report')
    return send_from_directory(directory=path_to_file, filename=filename)


@main.route('/', methods=['GET', 'POST'])
@main.route('/<brand>', methods=['POST', 'GET'])
def home(brand='samsung'):
    brand = get_class_by_tablename(brand)
    if g.user and request.method == 'POST':
        model_id_to_del = request.form['model-id-delete']
        obj_to_del = brand.query.get(model_id_to_del)
        if obj_to_del:
            db.session.delete(obj_to_del)
            db.session.commit()

    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search')
    models = paginate(brand.query, page)
    if search_query:
        # TODO remove pagination logical from brand.search
        models, total = brand.search(search_query, page, 3)
        models = paginate(models, page)
    return render_template('home/home.html', models=models, brand=brand)


@main.before_app_first_request
def setup_application():
    db.create_all()
