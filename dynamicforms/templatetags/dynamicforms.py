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
    """
    TODO: za skenslat?

    Simple filter to return the items of the dict. Useful when the dict may
    have a key 'items' which is resolved first in Django template dot-notation
    lookup. See DRF issue #4931
    Also see: https://stackoverflow.com/questions/15416662/django-template-loop-over-dictionary-items-with-items-as-key
    """
    return drftt.items(value)


@register.filter
def add_nested_class(value):
    return drftt.add_nested_class(value)


@register.filter
def format_value(value):
    # TODO: tegale je treba skenslat, ko bo narejena naloga #62 in #63
    return drftt.format_value(value)


@register.filter
def as_string(value):
    # TODO: tegale je treba skenslat, ko bo narejena naloga #62 in #63
    return drftt.as_string(value)


@register.filter
def as_list_of_strings(value):
    # TODO: tegale je treba skenslat, ko bo narejena naloga #62 in #63
    return drftt.as_list_of_strings(value)

# // just copy tags


@register.simple_tag
def render_form(serializer, template_pack=None, form_template=None):
    """
    Renders form from serializer. If form_template is given, then renderer will use that one, otherwise it will use what
    is defined in self.base_template (e.g.: »form.html«) from template_pack (e.g.: »dynamicforms/bootstrap/field/«)

    .. code-block:: django

       {% set_var template_pack=DF.TEMPLATE|add:'field' %}
       {% render_form serializer template_pack=template_pack %}

    TODO: template_pack should be deprecated? We now have a master template pack which takes care of everything

    :param serializer: Serializer object
    :param template_pack: template pack specified as directory where to find field & form templates
    :param form_template: form template file name to use. overrides all other template name declarations
    :return: rendered template
    """
    style = {'template_pack': template_pack} if template_pack else {}
    if form_template:
        style['form_template'] = form_template
    style['serializer'] = serializer

    renderer = HTMLFormRenderer()
    return renderer.render(serializer.data, None, {'style': style})


@register.simple_tag
def render_field(field, style):
    """
    Renders separate field. Style is a dict, that contains template_pack or form_tempate and rendered. It is defined when rendering form, so it is best to use that one. To do that dynamicforms should be loaded first. See example below.

    .. code-block:: django

       {% load dynamicforms %}
       {% for field in form %}
         {% if not field.read_only %}
           {% render_field field style=style %}
         {% endif %}
       {% endfor %}

    :param field: Serializer Field instance
    :param style: render parameters
    :return: rendered field template
    """
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
    """
    JSON serialises given variable. Use when you want to insert a variable directly into JavaScript

    :param value: variable to serialise
    :return: JSON serialised string
    """

    class Encoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Struct):
                return obj.__to_dict__()
            return super().default(obj)

    return mark_safe(jsonlib.dumps(value, cls=Encoder))
