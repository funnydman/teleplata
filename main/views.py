from flask import Blueprint, render_template, request

from .utils import get_class_by_tablename

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/<brand>')
def home(brand='samsung'):
    page = request.args.get('page', 1)
    models = get_class_by_tablename(brand).query.paginate(page=int(page),
                                                          per_page=8,
                                                          error_out=False)

    return render_template('home/home.html', models=models)


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@main.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500
