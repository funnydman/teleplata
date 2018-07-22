def get_form_data(request):
    """Getting model data from form"""
    result_dict = {}
    table_fields = ('model', 'power', 't_con', 'x_main',
                    'y_main', 'logic', 'invertor', 'y_scan')
    for field in table_fields:
        result_dict.update({field: request.form[field]})
    return result_dict
