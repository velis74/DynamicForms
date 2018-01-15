from django.template import loader
from .conditions import Condition
from ..util import field_set_value, val_to_js_const

if False:
    from dynamicforms.mixins.field import Field


class Action(object):
    TEMPLATE = ''

    def __init__(self, field: 'Field', condition: Condition, template=None) -> None:
        self.template = template or self.TEMPLATE
        self.field = field
        self.condition = condition

    def applies_to_field(self, field: 'Field'):
        """
        Returns True when this action has conditions that require given field's value to trigger. This determines
        whether action is rendered in given field's onchange event

        :param field: field against which the condition is supposed to trigger
        :return: bool
        """

        return self.condition.applies_to_field(field)

    def render(self, context: dict):
        """
        Generates javascript template code which executes every time given field's value changes. This code will
            evaluate conditions and perform the given action based on conditions' result

        the code has one JS variable available: formValue which is object with all form field values

        :param context: dict containing variables needed for rendering.
        """

        context['action_field'] = self.field
        context['condition'] = self.condition.render(context)

        return loader.render_to_string(self.get_template(context), context=context)

    def get_template(self, context: dict):
        """
        Returns the template file name to render to
        :param context: dict containing variables needed for rendering.
        """
        return context['form'].get_template_base(context) + self.template


class Visible(Action):
    """
    Toggling field visibility: If condition evaluates to true, field will be shown, otherwise it will be hidden
    """
    TEMPLATE = 'action_visible.js'


class SetValue(Action):
    """
    Setting field value: If condition evaluates to true, field value will be set, otherwise it will be left unchanged
    """
    def __init__(self, field: 'Field', condition: Condition, value, template=None) -> None:
        super().__init__(field, condition, template)
        self.value = value

    def render(self, context: dict) -> str:
        return '%s(%s);' % (field_set_value(context['field']), val_to_js_const(self.value))
