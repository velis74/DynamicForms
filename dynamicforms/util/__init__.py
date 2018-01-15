if False:
    from ..mixins.field import Field


def val_to_js_const(value) -> str:
    """
    Converts python variable to a JS constant
    :param value: python value to be converted to a JS constant
    :return: JS with the generated constant
    """
    if isinstance(value, (list, set)):
        return '[' + ', '.join((val_to_js_const(v) for v in value)) + ']'
    if isinstance(value, str):
        return "'%s'" % value.replace('\'', '\\\'')
    # TODO: support dates?
    return str(value)


def form_value(field: 'Field') -> str:
    """
    provides JS accessing current value of the given field
    :param field: field of which value should be retrieved
    :return: JS providing current field value
    """
    return 'formValue.' + field.name


def field_get_value(field: 'Field') -> str:
    """
    provides JS function name accessing current value of the given field
    :param field: field of which value should be retrieved
    :return: JS to function which will fill out current field's value into formValue object
    """
    return 'get_%s' % field.uuid.hex


def field_set_value(field: 'Field') -> str:
    """
    provides JS function name setting current value of the given field
    :param field: field of which value should be set
    :return: JS to function which set current field's value from formValue object property
    """
    return 'set_%s' % field.uuid.hex


def get_setting(name: str, default):
    """
    retrieves a setting from settings.py
    :param name: setting name. 'DFORM_' will be prepended to it
    :param default: default value if the setting is not there
    :return: setting value or default
    """
    from django.conf import settings
    return getattr(settings, 'DFORM_' + name, default)
