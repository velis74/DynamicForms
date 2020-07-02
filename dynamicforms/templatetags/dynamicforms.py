import json as jsonlib

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from rest_framework.templatetags import rest_framework as drftt
from rest_framework.utils.encoders import JSONEncoder

from ..action import TablePosition
from ..mixins import DisplayMode
from ..renderers import HTMLFormRenderer
from ..struct import Struct

register = template.Library()


@register.filter(name='dict_item')
def dict_item(d, k):
    """Returns the given key from a dictionary."""
    return d[k]


# just copy the template tags that are the same as we're not redeclaring them
# TODO: the following DRF filters pending removal?
# note that simply copying the filters didn't work: django kept complaining about parameters. So now it's verbatim copy
@register.filter
def items(value):
    """
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
    # TODO: this one pending removal on tasks #62 in #63 completion
    return drftt.format_value(value)


@register.filter
def as_string(value):
    # TODO: this one pending removal on tasks #62 in #63 completion
    return drftt.as_string(value)


@register.filter
def as_list_of_strings(value):
    # TODO: this one pending removal on tasks #62 in #63 completion
    return drftt.as_list_of_strings(value)


# // just copy tags


@register.simple_tag
def render_form(serializer, form_template=None):
    """
    Renders form from serializer. If form_template is given, then renderer will use that one, otherwise it will use what
    is defined in self.base_template (e.g.: »form.html«) from template_pack (e.g.: »dynamicforms/bootstrap/field/«)

    .. code-block:: django

       {% set_var template_pack=DYNAMICFORMS.template|add:'field' %}
       {% render_form serializer template_pack=template_pack %}

    :param serializer: Serializer object
    :param form_template: form template file name to use. overrides all other template name declarations
    :return: rendered template
    """
    style = {}
    if form_template:
        style['form_template'] = form_template
    style['serializer'] = serializer

    renderer = HTMLFormRenderer()
    return renderer.render(serializer.data, None, {'style': style})


@register.simple_tag
def render_field(field, style):
    """
    Renders separate field. Style is a dict, that contains template_pack or form_template and rendered. It is defined
    when rendering form, so it is best to use that one. To do that dynamicforms should be loaded first.

    See example below.

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


@register.simple_tag
def table_columns_count(serializer):
    """
    Returns number of columns including control columns

    :param serializer: Serializer
    :return: Number of all columns
    """
    actions = serializer.actions.renderable_actions(serializer)

    return (len([f for f in serializer.fields.values() if f.display_table == DisplayMode.FULL])
            + (1 if any(action.position == "rowend" for action in actions) else 0)
            + (1 if any(action.position == "rowstart" for action in actions) else 0))


@register.simple_tag(takes_context=True)
def render_table_commands(context, serializer, position, field_name=None, button_position=None):
    """
    Renders commands that are defined in serializers controls attribute.

    :param context: Context
    :param serializer: Serializer
    :param position: Position of command (See action.py->Action for more details)
    :param field_name: If position is left or right to the field, then this parameter must contain field name
    :param button_position: form button position one of (form, dialog, user-provided)
    :return: rendered command buttons. If table_header parameter is given and commands for position are defined,
        returns only rendered table header
    """
    ret = ''

    if position == 'onfieldchange':
        ret = serializer.actions.render_field_onchange(serializer)
        ret += serializer.actions.render_form_init(serializer)
    elif position == 'onfieldinit':
        ret += serializer.actions.render_field_init(serializer, field_name)
    elif position == 'form-buttons':
        ret += serializer.actions.render_form_buttons(serializer, button_position)
    else:
        table_header = None
        if position.startswith('thead_'):
            position = position[6:]
            table_header = _('Actions')

        positions = dict(
            onrowclick=(TablePosition.ROW_CLICK, TablePosition.ROW_RIGHTCLICK),
            header=(TablePosition.HEADER,),
            filterrowstart=(TablePosition.FILTER_ROW_START,),
            filterrowend=(TablePosition.FILTER_ROW_END,),
            rowstart=(TablePosition.ROW_START,),
            rowend=(TablePosition.ROW_END,),
            fieldleft=(TablePosition.FIELD_START,),
            fieldright=(TablePosition.FIELD_END,),
        )
        ret_tmp = serializer.actions.render_renderable_actions(positions[position], field_name, serializer)

        _position = positions[position][0]
        if ret_tmp and _position in (TablePosition.ROW_START, TablePosition.ROW_END,
                                     TablePosition.FILTER_ROW_START, TablePosition.FILTER_ROW_END):
            ret += ('<th>%s</th>' % table_header) if table_header else (
                '<td>%s</td>' % ret_tmp if _position not in (
                    TablePosition.FILTER_ROW_END, TablePosition.FILTER_ROW_START) else '<th>%s</th>' % ret_tmp)
        elif ret_tmp:
            ret += ret_tmp

    ret = '{% load static i18n %}' + ret

    return mark_safe(context.template.engine.from_string(ret).render(context))


@register.simple_tag(takes_context=True)
def field_to_serializer_and_data(context, serializer):
    """
    Adjusts context such that the nested serializer field becomes THE serializer

    :param serializer: field to be converted into context
    :return: nothing
    """
    if hasattr(serializer, 'child'):
        # this is a ListSerializer
        context.update(dict(serializer=serializer.child, data=serializer.value, **serializer.child.template_context))
    else:
        serializer._field._data = serializer.value  # The serializer has default values here
        context.update(dict(serializer=serializer, data=serializer.value, **serializer.template_context))
    return ''


@register.simple_tag(takes_context=True)
def get_data_template(context, context_data=None):
    """
    Returns template that should be used for rendering current serializer data

    :param context: template context (automatically provided by django)
    :return: template file name
    """
    if context_data:
        context = context_data
    serializer = context['serializer']
    return serializer.data_template


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
def set_var_conditional(context, condition=None, condition_var=None, compare=None, else_value=None, **kwds):
    """
    Sets the given variables to provided values. Kind of like the 'with' block, only it isn't a block tag

    :param context: template context (automatically provided by django)
    :param kwds: named parameters with their respective values
    :param condition_var: pair with compare to obtain True or False whether to use original assignment or else_value
    :param compare: pair with condition_var to obtain True or False whether to use original assignment or else_value
    :param condition: alternative to condition_var & compare: original assignment if truthy or else_value if falsy
    :param else_value: value to be assigned to the variable(s) when condition is falsy
    :return: this tag doesn't render
    """
    if condition_var is not None:
        condition = condition_var == compare
    for k, v in kwds.items():
        context[k] = v if condition else else_value
    return ''


@register.simple_tag(takes_context=False)
def iter_options_bound(field):
    return field.iter_options_bound(field.value) if hasattr(field, 'iter_options_bound') else []


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


@register.simple_tag(takes_context=True)
def dict_item_default(context, var, d, k, default):
    context[var] = d.get(k, default)

    return ''


@register.filter
def class_name(value):
    return value.__class__.__name__


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')


@register.filter
def startswith(text, starts):
    try:
        return text.startswith(starts)
    except:
        return False
