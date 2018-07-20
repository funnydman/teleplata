from flask import Blueprint, render_template, request, g

from main import db
from .utils import get_class_by_tablename

main = Blueprint('main', __name__)


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
    # TODO: add full-text search
    if search_query:
        models, total = brand.search(search_query, page, 3)
        test = [*db.metadata.tables.keys()]
        # we don't index user model
        test.remove('user')
        print(test)
        models = models.paginate(
            page=int(page),
            per_page=3,
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
