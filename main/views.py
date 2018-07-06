from flask import Blueprint, render_template, request

from .utils import get_class_by_tablename

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/<brand>', methods=['POST', 'GET'])
def home(brand='samsung'):
    page = request.args.get('page', 1)
    brand = get_class_by_tablename(brand)
    search_query = request.args.get('search')
    models = brand.query.paginate(
        page=int(page),
        per_page=15,
        error_out=False)
    # TODO: add full-text search
    if search_query:
        models = brand.query.filter(
            brand.model.contains(search_query)
        ).paginate(
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
