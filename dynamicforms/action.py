from typing import Iterable, List, Union
from enum import IntEnum
from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import Serializer
import uuid as uuid_module
from .settings import DYNAMICFORMS


class ActionBase(object):

    def __init__(self, action_js: str, name: Union[str, None] = None, serializer: Serializer = None):
        """
        :param action_js: JavaScript to execute when action is run
        :param name: name by which to recognise this action in further processing, e.g. Serializer.suppress_action
        :param serializer: bind to this serializer instance
        """
        self.name = name
        self.action_js = action_js
        assert self.action_js, 'When declaring action, it must declare action JavaScript to execute'
        # serializer will be set when obtaining a resolved copy
        self.serializer = serializer

    @property
    def action_id(self):
        return id(self)

    def copy_and_resolve_reference(self, serializer):
        raise NotImplementedError()

    def render(self, serializer: Serializer, **kwds):
        raise NotImplementedError()


class RenderableActionMixin(object):
    """
    Action that is rendered on screen
    """

    def __init__(self, label: str, title: str, icon: str = None):
        """
        :param label: Label for rendering to on screen control
        :param title: Hint text for on-screen control
        :param icon: optional icon to add to render
        """
        self.label = label
        self.title = title
        self.icon = icon


class TablePosition(IntEnum):
    HEADER = 0  # Table header of list view
    # On left click on table row (currently this renders only once per table.
    # We might need to add one that renders for each row
    ROW_CLICK = 1
    ROW_RIGHTCLICK = 2  # On right click on table row
    ROW_START = 3  # Additional control column on left side of table
    ROW_END = 4  # Additional control column on right side of table
    FIELD_START = 5  # On left side of field value
    FIELD_END = 6  # On right side of field value


class TableAction(ActionBase, RenderableActionMixin):

    def __init__(self, position: TablePosition, label: str, action_js: str,
                 title: Union[str, None] = None, icon: Union[str, None] = None, field_name: Union[str, None] = None,
                 name: Union[str, None] = None, serializer: Serializer = None):
        ActionBase.__init__(self, action_js, name, serializer)
        RenderableActionMixin.__init__(self, label, title, icon)
        self.position = position
        self.field_name = field_name

    def copy_and_resolve_reference(self, serializer: Serializer):
        return TableAction(self.position, self.label, self.action_js, self.title, self.icon, self.field_name, self.name,
                           serializer)

    def render(self, serializer: Serializer, **kwds):
        ret = rowclick = rowrclick = ''
        stop_propagation = 'if(event.stopPropagation){event.stopPropagation();}event.cancelBubble=true;'

        action_action = self.action_js
        if self.position != TablePosition.HEADER:
            # We need to do this differently because of dynamic page loading for tables: each time the serializer
            # has a different UUID
            action_action = action_action.replace('__TABLEID__',
                                                  "$(event.target).parents('table').attr('id').substr(5)")
        else:
            action_action = action_action.replace('__TABLEID__', "'" + str(serializer.uuid) + "'")

        if self.position == TablePosition.ROW_CLICK:
            rowclick = action_action
        elif self.position == TablePosition.ROW_RIGHTCLICK:
            rowrclick = action_action
        else:
            from uuid import uuid1

            btnid = uuid1()
            ret += '<button id="df-action-btn-{btnid}" type="button" class="btn btn-info" ' \
                   'onClick="{stop_propagation} {action}">{icon_def}{label}</button>'. \
                format(btnid=btnid, stop_propagation=stop_propagation, action=action_action,
                       label=self.label,
                       icon_def='<img src="{icon}"/>'.format(icon=self.icon) if self.icon else '')
            if DYNAMICFORMS.jquery_ui:
                ret += '<script type="application/javascript">$("#df-action-btn-{btnid}").button();</script>'\
                    .format(btnid=btnid)

        if self.position in (TablePosition.ROW_CLICK, TablePosition.ROW_RIGHTCLICK):
            if rowclick != '':
                ret += "$('#list-{uuid}').find('tbody').click(" \
                       "function(event) {{ \n{stop_propagation} \n{action} \nreturn false;\n}});\n". \
                    format(stop_propagation=stop_propagation, action=rowclick, uuid=serializer.uuid)
            if rowrclick != '':
                ret += "$('#list-{uuid}').find('tbody').contextmenu(" \
                       "function(event) {{ \n{stop_propagation} \n{action} \nreturn false;\n}});\n". \
                    format(stop_propagation=stop_propagation, action=rowrclick, uuid=serializer.uuid)
            if ret != '':
                ret = '<script type="application/javascript">%s</script>' % ret

        elif ret != '':
            ret = '<div class="dynamicforms-actioncontrol float-{direction} pull-{direction}">{ret}</div>'.format(
                ret=ret, direction='left' if self.position == TablePosition.FIELD_START else 'right'
            )

        return ret


class FieldChangeAction(ActionBase):

    def __init__(self, tracked_fields: Iterable[str], action_js: str, name: Union[str, None] = None,
                 serializer: Serializer = None):
        super().__init__(action_js, name, serializer)
        self.tracked_fields = tracked_fields
        assert self.tracked_fields, 'When declaring an action, it must track at least one form field'
        if serializer:
            self.tracked_fields = [self._resolve_reference(f) for f in self.tracked_fields]

    def _resolve_reference(self, ref):
        from .mixins import UUIDMixIn

        if isinstance(ref, uuid_module.UUID):
            return str(ref)
        elif isinstance(ref, UUIDMixIn):
            # TODO unit tests!!!
            # TODO test what happens if the Field instance given is from another serializer
            # TODO test what happens when Field instance is actually a Serializer (when should onchange trigger for it?)
            return ref.uuid
        elif isinstance(ref, str) and ref in self.serializer.fields:
            return self.serializer[ref].uuid
        elif isinstance(ref, str) and '.' in ref:
            # This supports nested serializers and fields with . notation, e.g. master_serializer_field.child_field
            f = self.serializer
            for r in ref.split('.'):
                f = f[r]
            return f.uuid
        raise Exception('Unknown reference type for Action tracked field (%r)' % ref)

    def copy_and_resolve_reference(self, serializer: Serializer):
        return FieldChangeAction(self.tracked_fields, self.action_js, self.name, serializer)

    def render(self, serializer: Serializer, **kwds):
        res = 'var action_func{0.action_id} = {0.action_js};\n'.format(self)
        for tracked_field in self.tracked_fields:
            res += "dynamicforms.registerFieldAction('{ser.uuid}', '{tracked_field}', action_func{s.action_id});\n"\
                .format(ser=serializer, tracked_field=tracked_field, s=self)
        return res


class FormInitAction(ActionBase):

    def copy_and_resolve_reference(self, serializer: Serializer):
        return FormInitAction(self.action_js, self.name, serializer)

    def render(self, serializer: Serializer, **kwds):
        # we need window.setTimeout because at the time of form generation, the initial fields value collection
        # hasn't been done yet
        return 'window.setTimeout(function() {{ {0.action_js} }}, 1);;\n'.format(self)


class FieldInitAction(FieldChangeAction):

    def copy_and_resolve_reference(self, serializer: Serializer):
        return FieldInitAction(self.tracked_fields, self.action_js, self.name, serializer)

    def render(self, serializer: Serializer, **kwds):
        # we need window.setTimeout because at the time of form generation, the initial fields value collection
        # hasn't been done yet
        return 'window.setTimeout(function() {{ {0.action_js} }}, 1);;\n'.format(self)


class Actions(object):

    def __init__(self, *args, add_default_crud: bool = False, add_default_filter: bool = False) -> None:
        super().__init__()
        self.actions = list(args)  # type: List[ActionBase]
        if add_default_crud:
            self.actions.append(
                TableAction(TablePosition.HEADER, _('+ Add'), title=_('Add new record'), name='add',
                            action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                                      ", 'record', __TABLEID__);")
            )
            self.actions.append(
                TableAction(TablePosition.ROW_CLICK, _('Edit'), title=_('Edit record'), name='edit',
                            action_js="dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' "
                                      "format='html' %}'.replace('__ROWID__', $(event.target).parents('tr')."
                                      "attr('data-id')), 'record', __TABLEID__);")
            )
            self.actions.append(
                TableAction(TablePosition.ROW_END, label=_('Delete'), title=_('Delete record'), name='delete',
                            action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                                      "{{row.id}}, 'record', __TABLEID__);"))
        if add_default_filter:
            self.actions.append(TableAction(TablePosition.HEADER, label=_('Filter'), title=_('Filter'), name='filter',
                                            action_js="dynamicforms.defaultFilter(event);"))

    def get_resolved_copy(self, serializer) -> 'Actions':
        """
        Returns a copy of declared actions bound to the serializer
        :param serializer: serializer the copy will be bound to
        :return:
        """
        if not isinstance(serializer, Serializer):
            return Actions()

        actions = [a.copy_and_resolve_reference(serializer) for a in self.actions]

        # move actions from Field to Serializer
        actions.extend([a.copy_and_resolve_reference(serializer)
                        for field in serializer.fields.values()
                        for a in getattr(field, 'actions', Actions()).actions])

        return Actions(*actions)

    def render_field_onchange(self, serializer):
        """
        renders all field onchange actions needed for dynamicforms.registerFieldAction() function

        :return: the actions rendered as template string
        """
        res = ''
        for action in self.actions:
            if isinstance(action, FieldChangeAction) and not isinstance(action, FieldInitAction):
                res += action.render(serializer)
        return res

    def render_form_init(self, serializer):
        """
        renders the function which will analyse initial form data and hide appropriate fields

        :return: the actions rendered as template string
        """
        res = ''
        for action in self.actions:
            if isinstance(action, FormInitAction):
                res += action.render(serializer)
        return res

    def render_field_init(self, serializer, field_name: str):
        """
        renders function that will initialise the field being rendered

        :return: the actions rendered as template string
        """
        res = ''
        for action in self.actions:
            if isinstance(action, FieldInitAction) and field_name in action.tracked_fields:
                res += action.render(serializer)
        return res

    def renderable_actions(self, serializer: Serializer):
        request = serializer.context.get('request', None)
        viewset = serializer.context.get('view', None)
        return (a for a in self.actions
                if isinstance(a, TableAction) and not serializer.suppress_action(a, request, viewset))

    def render_renderable_actions(self, allowed_positions: Iterable[TablePosition], field_name: str,
                                  serializer: Serializer):
        """
        Returns those actions that are not suppressed
        :return: List[Action]
        """
        res = ''

        for action in self.renderable_actions(serializer):
            if action.position in allowed_positions and (field_name is None or field_name == action.field_name):
                res += action.render(serializer)
        return res

    def __iter__(self):
        return iter(self.actions)


"""
tipi akcij
    crud (new, edit, delete, view detail)
    on field change
    on form display (initial fields hiding)
    dialog / form manipulation (cancel entry, submit entry)
    custom actions

kako se akcije renderajo
    gumb / link                    -> html control
    onclick / onrightclick / onkey -> JS event
    on field change                -> JS event (depends on field / position)


akcije na formi / dialogu
    control column (start, end of row, any position?)  -> HTML control
    table header / footer          -> html control
    table field left / right       -> html control
    form field left / right        -> html control
    form top, form bottom          -> html control
    custom pozicija  (programer pokliče render funkcijo z nekim custom tekstom, namesto z enum vrednostjo)



    ali morajo vedeti, na čem so?
    pri formi imamo submit, pri dialogu pa dynamicforms.SubmitForm, se pravi, da je render drugačen
    pri tabeli row id, morda row data?


    podatki, ki so lahko na voljo:
    parent serializer
    serializer
    row data
    form data --> serializer
"""
