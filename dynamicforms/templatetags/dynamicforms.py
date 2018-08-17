from django import template
from ..renderers import HTMLFormRenderer
from rest_framework.templatetags import rest_framework as drftt

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
