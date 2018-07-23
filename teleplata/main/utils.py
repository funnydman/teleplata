from datetime import datetime

import pdfkit
from flask import render_template

from . import common, db


def get_class_by_tablename(tablename):
    """Return class reference mapped to table.

    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for c in db.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c


def get_pdf_report(source, destination):
    models_by_brand_dict = {}
    for brand in common.BRAND_LIST:
        models = get_class_by_tablename(brand).query.all()
        if not models_by_brand_dict.get(brand):
            models_by_brand_dict.update({brand: models})
    options = {
        'footer-right': '[page]'
    }
    # TODO should we add time to datetime string?
    current_date = datetime.utcnow().strftime("%Y_%m_%d")
    filename = 'report-' + current_date + '.pdf'
    template = render_template(f"{source}", models=models_by_brand_dict)
    pdfkit.from_string(template, f'{destination}/{filename}', options=options)
    return filename


def paginate(to_paginate, page, per_page=15, error_out=False):
    return to_paginate.paginate(page=int(page),
                                per_page=per_page,
                                error_out=error_out)
