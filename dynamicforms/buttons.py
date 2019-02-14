import uuid
from typing import Iterable
from enum import IntEnum

from django.utils.translation import ugettext_lazy as _


class FormButtonTypes(IntEnum):
    CANCEL = 1
    SAVE = 2
    CUSTOM = 3


DEFAULT_LABELS = {
    FormButtonTypes.CANCEL: _('Cancel'),
    FormButtonTypes.SAVE: _('Save changes'),
    FormButtonTypes.CUSTOM: _('Custom'),
}


class Button(object):
    """
    Defines btn_type, label and action for FormButtons

    :param btn_type: Button type
    :param label: Label for button
    :param js:Code that executes written in Javascript
    """

    def __init__(self, btn_type, label: str = None, btn_classes: str = None, js=None):
        self.uuid = uuid.uuid1()
        self.btn_type = btn_type
        self.label = label or DEFAULT_LABELS.get(btn_type, FormButtonTypes.CUSTOM)
        self.js = js
        self.btn_classes = btn_classes or 'btn-secondary'


class FormButtons(object):
    """
    Used for defining buttons in dialog.
    Default buttons are Cancel and Save changes.
    """

    def __init__(self, buttons: Iterable[Button] = None, add_default_cancel: bool = False,
                 add_default_save: bool = False):
        self.buttons = [] if buttons is None else buttons
        if isinstance(self.buttons, tuple):
            self.buttons = list(self.buttons)

        if add_default_cancel:
            self.buttons.append(Button(btn_type=FormButtonTypes.CANCEL))
        if add_default_save:
            self.buttons.append(Button(btn_type=FormButtonTypes.SAVE))
