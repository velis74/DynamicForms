from typing import Iterable

from django.utils.translation import ugettext_lazy as _


class Action(object):
    """
    Defines appearance and action for ActionControls

    :param label: Label for button
    :param title: Hint text for button
    :param icon: Path to icon image for button
    :param action: Code that executes written in Javascript. It also supports django templates
    :param position: Defines where control is placed. All controls positions are:

     * header - Table header of list view
     * rowclick - On left click on table row
     * rowrightclick - On right click on table row
     * rowstart - Additional control column on left side of table
     * rowend - Additional control column on right side of table
     * fieldleft - On left side of field value
     * fieldright -  On right side of field value
    :param field_name: If position is set to fieldleft or fieldright then this parameter must contain name of field
      where commands will be set
    """

    def __init__(self, label, title, icon, action, position, field_name=None):
        self.label = label
        self.title = title
        self.icon = icon
        self.action = action
        self.position = position
        self.field_name = field_name


class ActionControls(object):
    """
    Used fo defining controls on table view.
    Default controls are add record button on table header, edit record on row click and delete record button on right
    side of row.
    If add_default_filter == True, than filter button is shown in table header
    """

    def __init__(self, actions: Iterable[Action] = None, add_default_crud: bool = False,
                 add_default_filter: bool = False):
        self.actions = [] if actions is None else actions
        if isinstance(self.actions, tuple):
            self.actions = list(self.actions)

        if add_default_crud:
            self.actions.append(
                Action(label=_('+ Add'), title=_('Add new record'), icon='', position='header',
                       action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}', refreshType='record');"))
            self.actions.append(
                Action(label=_('Edit'), title=_('Edit record'), icon='', position='rowclick',
                       action="dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' format='html'"
                              " %}'.replace('__ROWID__', $(event.target.parentElement).attr('data-id')), refreshType='record');"))
            self.actions.append(
                Action(label=_('Delete'), title=_('Delete record'), icon='', position='rowend',
                       action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                       + "deleteThisRow={{row.id}}, refreshType='record');"))
        if add_default_filter:
            self.actions.append(Action(label=_('Filter'), title=_('Filter'), icon='', position='header',
                                       action="dynamicforms.defaultFilter(event);"))
