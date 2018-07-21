import os
from datetime import datetime

import pdfkit
from flask import Blueprint, render_template, request, g, send_from_directory
from flask import current_app

from main import db
from .utils import get_class_by_tablename

main = Blueprint('main', __name__)

brands_list = ['samsung', 'lg', 'tomson']


def get_pdf_report():
    models_by_brand_dict = {}
    for brand in brands_list:
        models = get_class_by_tablename(brand).query.all()
        if not models_by_brand_dict.get(brand):
            models_by_brand_dict.update({brand: models})
    # TODO option footer-right doesn't work. Why?
    # TODO fix problem with page break
    options = {
        'footer-right': '[page]'
    }
    # TODO should we add time to datetime string?
    current_date = datetime.utcnow().strftime("%Y_%m_%d")
    filename = 'report-' + current_date + '.pdf'
    template = render_template('report/report.html', models=models_by_brand_dict)
    pdfkit.from_string(template, f'templates/report/{filename}', options=options)

    return filename


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
    models = brand.query.paginate(
        page=int(page),
        per_page=15,
        error_out=False)
    if search_query:
        models, total = brand.search(search_query, page, 3)
        models = models.paginate(
            page=int(page),
            per_page=15,
            error_out=False)
    return render_template('home/home.html', models=models, brand=brand)


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@main.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


@main.before_app_first_request
def setup_application():
    db.create_all()
