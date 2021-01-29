import json


def validation_error_convertor(validation_errors):

    errors = json.loads(validation_errors)
    new_errors = dict()

    for error in errors:
        new_errors[error] = errors[error][0]['message']

    return new_errors
