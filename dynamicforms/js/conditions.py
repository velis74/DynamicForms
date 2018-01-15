from ..util import val_to_js_const, form_value
from django.template import loader
if False:
    from dynamicforms.mixins.field import Field


class Condition(object):
    TEMPLATE = ''

    def __init__(self, field: 'Field', template=None) -> None:
        self.template = template or self.TEMPLATE
        self.field = field

    def applies_to_field(self, field: 'Field'):
        """
        Returns True when this condition requires given field's value to trigger. This determines whether action is
        rendered in given field's onchange event

        :param field: field against which the condition is supposed to trigger
        :return: bool
        """
        return field == self.field

    def render(self, context: dict):
        """
        Generates javascript template code which executes every time given field's value changes. This code will be
        inserted into a function body so it must end with a return statement (returning a boolean)

        the code has one JS variable available: formValue which is object with all form field values

        :param context: dict containing variables needed for rendering.
        """
        return loader.render_to_string(self.get_template(context), context=context)

    def get_template(self, context: dict):
        return context['form'].get_template_base(context) + self.template


class CFieldValue(Condition):
    """
    Evaluates field value against given constant.
    """
    TEMPLATE = 'cond_field_value.js'

    def __init__(self, field: 'Field', value, template=None) -> None:
        """
        :param value: accepts a constant or list of constants.
                      if field value matches value (values in the list), condition triggers
        TODO: could also accept another field. matching to another field's value then triggers
        """
        super().__init__(template, field)
        self.value = value

    def render(self, context: dict):
        context.update(dict(
            matching_values=val_to_js_const(self.value),
            matching_values_is_list=isinstance(self.value, (list, set)),
            field_value=form_value(self.field),
        ))
        return super().render(context)

# TODO: Composite conditions (and, or, braces)
# TODO: support condition that triggers when multiple fields match to given values, e.g. field1 == 1 && field2 == 'b'
