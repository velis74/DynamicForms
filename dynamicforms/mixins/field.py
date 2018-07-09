from uuid import UUID, uuid1
from django.template import loader
from ..js.actions import Action
from typing import List, Dict, Union, Callable
from enum import IntEnum as Enum
from dynamicforms.util import form_value


class Field(object):
    TEMPLATE = 'field_input.html'

    # noinspection PyUnreachableCode
    if False:
        # provided by implementations, here only for IDE to recognise the member
        name = ''

    def __init__(self, uuid: UUID=None, suppress: Union(bool, Callable[[], bool])=False,
                 actions: List[Action]=None, template=None):
        """
        :param uuid: uuid is the field's unique HTML id used to distinguish it in JS operations
        :param suppress: Determines whether the field is included in the form at all.
            Accepts a boolean or a function(initial_values) to return a boolean result
        :param actions: performs actions based on conditions.
        :param template: template to use for rendering
        """
        self.template = template or self.TEMPLATE
        self.uuid = uuid or uuid1()
        self.suppress = suppress
        self.actions = []
        for action in (actions or []):
            assert isinstance(action, Action)
            self.add_action(action)

    def add_action(self, action: Action):
        self.actions.append(action)

    def render(self, context: dict):
        """
        Generates HTML template code which renders the field either in specified mode
            full mode: standard form field rendering with full functionality. Full mode must also generate field
                getter and setter functions. Please see template tags field_unique_ident
            preview mode: context variable 'preview' will be set to True. Used when rendering a read only form preview
                or a table row. This mode should render to lean HTML: go easy on controls & JavaScript. Maybe also
                resolve foreign keys from id to something more meaningful, like a name

        :param context: dict containing variables needed for rendering.
        """

        context['field'] = self

        return loader.render_to_string(self.get_template(context), context=context)

    def get_template(self, context: dict):
        """
        Returns the template file name to render to
        :param context: dict containing variables needed for rendering.
        """
        return context['form'].get_template_base(context) + self.template


class FieldTemplate(Enum):
    FIELD = 0
    SET_VALUE = 1
    GET_VALUE = 2


class InputField(Field):
    """
    Field that handles its input through standard HTML input widget
    """
    def __init__(self, uuid: UUID=None, suppress: Union(bool, Callable[[], bool])=False,
                 actions: List[Action]=None, template=None,
                 input_attributes: Dict[str, str]=None):
        super().__init__(uuid, suppress, actions, template)
        self.input_attributes = input_attributes
