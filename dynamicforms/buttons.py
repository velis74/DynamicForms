from typing import Iterable
from enum import IntEnum

from django.utils.translation import ugettext_lazy as _


class Button(object):
    """
    Defines btn_type, label and action for FormButtons

    :param btn_type: Button type
    :param label: Label for button
    :param js:Code that executes written in Javascript
    """

    def __init__(self, btn_type, label, js=None):
        self.btn_type = btn_type
        self.label = label
        self.js = js


class FormButtonTypes(IntEnum):
    CANCEL = 1
    SAVE = 2
    CUSTOM = 3


class FormButtons(object):
    """
    Used for defining buttons in dialog.
    Default buttons are Cancel and Save changes.
    """

    def __init__(self, buttons: Iterable[Button] = None, add_default_buttons: bool = False):
        self.buttons = [] if buttons is None else buttons
        if isinstance(self.buttons, tuple):
            self.buttons = list(self.buttons)

        if add_default_buttons:
            self.buttons.append(Button(btn_type=FormButtonTypes.CANCEL, label=_('Cancel')))
            self.buttons.append(Button(btn_type=FormButtonTypes.SAVE, label=_('Save changes')))
