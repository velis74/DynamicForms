import json as jsonlib

from django import template
from django.utils.safestring import mark_safe

from rest_framework.templatetags import rest_framework as drftt
from rest_framework.utils.encoders import JSONEncoder
from ..renderers import HTMLFormRenderer
from ..struct import Struct


register = template.Library()


# just copy the template tags that are the same as we're not redeclaring them
# note that simply copying the filters didn't work: django kept complaining about parameters. So now it's verbatim copy
@register.filter
def items(value):
    return drftt.items(value)


@register.filter
def add_nested_class(value):
    return drftt.add_nested_class(value)


@register.filter
def format_value(value):
    return drftt.format_value(value)


@register.filter
def as_string(value):
    return drftt.as_string(value)


@register.filter
def as_list_of_strings(value):
    return drftt.as_list_of_strings(value)

# // just copy tags


@register.simple_tag
def render_form(serializer, template_pack=None, form_template=None):
    style = {'template_pack': template_pack} if template_pack else {}
    if form_template:
        style['form_template'] = form_template
    style['serializer'] = serializer

    renderer = HTMLFormRenderer()
    return renderer.render(serializer.data, None, {'style': style})


@register.simple_tag
def render_field(field, style):
    renderer = style.get('renderer', HTMLFormRenderer())
    return renderer.render_field(field, style)


@register.simple_tag(takes_context=True)
def set_var(context, **kwds):
    """
    Sets the given variables to provided values. Kind of like the 'with' block, only it isn't a block tag
    :param context: template context (automatically provided by django)
    :param kwds: named parameters with their respective values
    :return: this tag doesn't render
    """
    for k, v in kwds.items():
        context[k] = v
    return ''


@register.simple_tag(takes_context=True)
def set_var_conditional(context, condition=None, else_value=None, **kwds):
    """
    Sets the given variables to provided values. Kind of like the 'with' block, only it isn't a block tag
    :param context: template context (automatically provided by django)
    :param kwds: named parameters with their respective values
    :param condition: a value which specifies the original assignment if truthy or else_value if falsy
    :param else_value: value to be assigned to the variable(s) when condition is falsy
    :return: this tag doesn't render
    """
    for k, v in kwds.items():
        context[k] = v if condition else else_value
    return ''


@register.filter
def json(value):

    class Encoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Struct):
                return obj.__to_dict__()
            return super().default(obj)

    return mark_safe(jsonlib.dumps(value, cls=Encoder))
