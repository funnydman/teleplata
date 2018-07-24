from teleplata.main.common import MODEL_FIELDS


def get_form_data(request):
    """Getting model data from form"""
    result_dict = {}
    table_fields = MODEL_FIELDS
    for field in table_fields:
        if request.form[field]:
            result_dict.update({field: request.form[field]})
    return result_dict
