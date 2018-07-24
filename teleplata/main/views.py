import os

from flask import Blueprint, render_template, request, g, send_from_directory
from flask import current_app

from . import db
from .utils import get_class_by_tablename, get_pdf_report, paginate

main = Blueprint('main', __name__)


@main.route('/report/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    report_folder = os.path.join(current_app.template_folder, 'report')
    filename = get_pdf_report('report/report.html', report_folder)
    return send_from_directory(directory=report_folder, filename=filename)


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
    # search_query = request.args.get('search')
    models = paginate(brand.query, page)
    return render_template('home/home.html', models=models, brand=brand)


@main.before_app_first_request
def setup_application():
    db.create_all()
