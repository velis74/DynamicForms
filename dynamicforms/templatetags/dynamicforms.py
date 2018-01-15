from django.template.defaulttags import register
from .. import util


@register.simple_tag()
def field_unique_ident(field):
    """
    Generates field globally unique identifier for use in various variables, function names, etc. dealing with the field
    No need to worry about unique function names for fields
    :param field: see util.field_get_value
    :return: template JS code
    """
    return field.uuid.hex


"""
@register.simple_tag(takes_context=True)
def field_get_value(context, field):
    return util.field_get_value(field)
"""
