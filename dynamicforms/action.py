import uuid as uuid_module
from enum import IntEnum
from typing import Iterable, List, Union

from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer

from .settings import DYNAMICFORMS


class ActionBase(object):
    def __init__(self, name: str, serializer: Serializer = None, action=None):
        """
        :param name: name by which to recognise this action in further processing, e.g. Serializer.suppress_action
        :param serializer: bind to this serializer instance
        :param action: this is a dict specifying how the vue renderer should render the action. several modes are
           supported:
           dict(func_name, params): calls window.func_name(params) (func_name can contain dots which will be resolved)
           dict(href): action is actually a href - the browser will redirect to the given href
           dict(href, router_name=True): action is a href to a Vue router named path. href will be resolved from name
        """
        assert name is not None, "Action name must not be None"
        self.name = name
        self.action = action
        # serializer will be set when obtaining a resolved copy
        self.serializer = serializer

    @property
    def action_id(self):
        return id(self)

    def copy_and_resolve_reference(self, serializer):
        raise NotImplementedError()

    def render(self, serializer: Serializer, **kwds):
        raise NotImplementedError()

    @staticmethod
    def prepare_string(string, encode=True):
        """
        Replaces curly brackets with some special string so there is no problem when string.format() is called

        :param string: String in which program searches for curly brackets
        :param encode: True: replaces brackets with special string, False: the other way around
        :return:
        """
        if not string:
            return ""
        replaces = {"{": "´|curl_brack_start|`", "}": "´|curl_brack_end|`"}
        if not encode:
            replaces = dict([(value, key) for key, value in replaces.items()])

        for key, val in replaces.items():
            string = string.replace(key, val)
        return string

    def as_component_def(self):
        return {k: getattr(self, k) for k in ("name", "action")}


class TablePosition(IntEnum):
    HEADER = 0  # Table header of list view
    FILTER_ROW_START = 7  # Alternative to HEADER: command is placed in filter row, actions column at start of line
    FILTER_ROW_END = 8  # Alternative to HEADER: command is placed in filter row, actions column at end of line
    # On left click on table row (currently this renders only once per table.
    # We might need to add one that renders for each row
    ROW_CLICK = 1
    ROW_RIGHTCLICK = 2  # On right click on table row
    ROW_START = 3  # Additional control column on left side of table
    ROW_END = 4  # Additional control column on right side of table
    FIELD_START = 5  # On left side of field value
    FIELD_END = 6  # On right side of field value


class FormButtonTypes(IntEnum):
    CANCEL = 1
    SUBMIT = 2
    CUSTOM = 3


class RenderableActionMixin(object):
    """
    Action that is rendered on screen
    """

    def __init__(
        self,
        label: str,
        title: str,
        icon: str = None,
        btn_classes: Union[str, dict, None] = None,
        display_style: Union[dict, None] = None,
    ):
        """
        :param label: Label for rendering to on screen control
        :param title: Hint text for on-screen control
        :param icon: optional icon to add to render
        :param btn_classes: optional class(es) of button. if variable is dict and key 'replace' have value True,
         then default class will be replaced with class(es) that are under key 'classes'. In other case class(es) will
         be just added to default class
        :param display_style: How is action rendered - Button or non button, only icon, only label, bot icon and label
        """
        self.label = label
        self.title = title
        self.icon = icon
        self.btn_classes = btn_classes
        self.display_style = display_style

    def as_component_def(self):
        return dict(
            label=self.label,
            title=self.title,
            icon=self.icon,
            classes=self.btn_classes,
            displayStyle=self.display_style,
        )

    @staticmethod
    def def_display_style(
        table_position: Union[TablePosition, None] = None, form_button: Union[FormButtonTypes, None] = None
    ):
        if table_position == TablePosition.HEADER:
            return dict(
                md=dict(asButton=True, showLabel=True, showIcon=True),
                xs=dict(asButton=True, showLabel=False, showIcon=True),
            )
        elif table_position in (
            TablePosition.FILTER_ROW_START,
            TablePosition.FILTER_ROW_END,
            TablePosition.ROW_START,
            TablePosition.ROW_END,
        ):
            return dict(xs=dict(asButton=True, showLabel=False, showIcon=True))
        elif table_position in (TablePosition.FIELD_START, TablePosition.FIELD_END):
            return dict(xs=dict(asButton=False, showLabel=False, showIcon=True))
        elif form_button in (FormButtonTypes.SUBMIT, FormButtonTypes.CANCEL, FormButtonTypes.CUSTOM):
            return dict(xs=dict(asButton=True, showLabel=True, showIcon=False))
        return None


class TableAction(ActionBase, RenderableActionMixin):
    def __init__(
        self,
        position: TablePosition,
        label: str,
        title: Union[str, None] = None,
        icon: Union[str, None] = None,
        field_name: Union[str, None] = None,
        name: Union[str, None] = None,
        serializer: Serializer = None,
        btn_classes: Union[str, dict, None] = None,
        action=None,
        display_style=None,
    ):
        ActionBase.__init__(self, name, serializer, action=action)
        RenderableActionMixin.__init__(
            self, label, title, icon, btn_classes, display_style or self.def_display_style(table_position=position)
        )
        self.position = position
        self.field_name = field_name

    def copy_and_resolve_reference(self, serializer: Serializer):
        return TableAction(
            self.position,
            self.label,
            self.title,
            self.icon,
            self.field_name,
            self.name,
            serializer,
            self.btn_classes,
            action=self.action,
            display_style=self.display_style,
        )

    def to_component_params(self, row_data, serializer):
        """
        generates a dict with parameters for component that is going to represent this action.
        none means don't render / activate this action on this row

        :param row_data:
        :param serializer:
        :return:
        """
        if self.position in (TablePosition.HEADER, TablePosition.FILTER_ROW_START, TablePosition.FILTER_ROW_END):
            return self.name, None
        return self.name, {}

    def as_component_def(self):
        res = dict(position=self.position.name, field_name=self.field_name)
        res.update(ActionBase.as_component_def(self))
        res.update(RenderableActionMixin.as_component_def(self))
        return res

    def render(self, serializer: Serializer, **kwds):
        ret = rowclick = rowrclick = ""
        stop_propagation = "dynamicforms.stopEventPropagation(event);"

        action_action = self.prepare_string("")  # TODO maybe: self.action_js. more likely this just needs to be removed
        if self.position != TablePosition.HEADER:
            # We need to do this differently because of dynamic page loading for tables: each time the serializer
            # has a different UUID
            action_action = action_action.replace(
                "__TABLEID__", "$(event.target).parents('table').attr('id').substring(5)"
            )
        else:
            action_action = action_action.replace("__TABLEID__", "'" + str(serializer.uuid) + "'")

        if self.position == TablePosition.ROW_CLICK:
            rowclick = action_action
        elif self.position == TablePosition.ROW_RIGHTCLICK:
            rowrclick = action_action
        else:

            def get_btn_class(default_class, additional_class):
                classes = default_class.split(" ")
                if additional_class:
                    if isinstance(additional_class, dict):
                        if additional_class.get("replace", False):
                            classes = []
                        additional_class = additional_class.get("classes", "").split(" ")
                    else:
                        additional_class = additional_class.split(" ")
                    classes.extend(additional_class)
                return " ".join(classes)

            button_name = (' name="btn-%s" ' % self.name) if self.name else ""
            btn_class = get_btn_class("btn btn-info", self.btn_classes)

            btnid = uuid_module.uuid1()
            ret += (
                '<button id="df-action-btn-{btnid}" type="button" class="{btn_class}" title="{title}"{button_name}'
                'onClick="{stop_propagation} {action}">{icon_def}{label}</button>'.format(
                    btnid=btnid,
                    stop_propagation=stop_propagation,
                    action=action_action,
                    btn_class=btn_class,
                    label=self.prepare_string(self.label),
                    title=self.prepare_string(self.title),
                    icon_def='<img src="{icon}"/>'.format(icon=self.icon) if self.icon else "",
                    button_name=button_name,
                )
            )
            if DYNAMICFORMS.jquery_ui:
                ret += '<script type="application/javascript">$("#df-action-btn-{btnid}").button();</script>'.format(
                    btnid=btnid
                )

        if self.position in (TablePosition.ROW_CLICK, TablePosition.ROW_RIGHTCLICK):
            if rowclick != "":
                ret += (
                    "$('#list-{uuid}').find('tbody').click("
                    "function(event) {{ \n{stop_propagation} \n{action} \nreturn false;\n}});\n".format(
                        stop_propagation=stop_propagation, action=rowclick, uuid=serializer.uuid
                    )
                )
            if rowrclick != "":
                ret += (
                    "$('#list-{uuid}').find('tbody').contextmenu("
                    "function(event) {{ \n{stop_propagation} \n{action} \nreturn false;\n}});\n".format(
                        stop_propagation=stop_propagation, action=rowrclick, uuid=serializer.uuid
                    )
                )
            if ret != "":
                ret = '<script type="application/javascript">%s</script>' % ret

        elif ret != "":
            ret = '<div class="dynamicforms-actioncontrol float-{direction} pull-{direction}">{ret}</div>'.format(
                ret=ret, direction="left" if self.position == TablePosition.FIELD_START else "right"
            )

        return self.prepare_string(ret, False)


class FieldChangeAction(ActionBase):
    def __init__(
        self, tracked_fields: Iterable[str], name: Union[str, None] = None, serializer: Serializer = None, action=None
    ):
        super().__init__(name, serializer, action=action)
        self.tracked_fields = tracked_fields or []
        # assert self.tracked_fields, 'When declaring an action, it must track at least one form field'
        if serializer:
            self.tracked_fields = [self._resolve_reference(f) for f in self.tracked_fields]

    def to_component_params(self, row_data, serializer):
        """
        generates a dict with parameters for component that is going to represent this action.
        none means don't render / activate this action on this row

        :param row_data:
        :param serializer:
        :return:
        """
        # perhaps this function is misnamed: it should be row_render_params, because only the row-level properties are
        #  processed
        return self.name, None

    def as_component_def(self):
        res = dict(position="VALUE_CHANGED", tracked_fields=list(self.tracked_fields))
        res.update(ActionBase.as_component_def(self))
        return res

    def _resolve_reference(self, ref):
        from .mixins import FieldRenderMixin

        if isinstance(ref, uuid_module.UUID):
            return str(ref)
        elif isinstance(ref, FieldRenderMixin):
            # TODO unit tests!!!
            # TODO test what happens if the Field instance given is from another serializer
            # TODO test what happens when Field instance is actually a Serializer (when should onchange trigger for it?)
            return ref.uuid
        elif isinstance(ref, str) and ref in self.serializer.fields:
            return self.serializer.fields[ref].uuid
        elif isinstance(ref, str) and "." in ref:
            # This supports nested serializers and fields with . notation, e.g. master_serializer_field.child_field
            f = self.serializer
            for r in ref.split("."):
                f = f.fields[r]
            return f.uuid
        raise Exception("Unknown reference type for Action tracked field (%r)" % ref)

    def copy_and_resolve_reference(self, serializer: Serializer):
        return FieldChangeAction(self.tracked_fields, self.name, serializer)

    def render(self, serializer: Serializer, **kwds):
        res = "var action_func{0.action_id} = {0.action_js};\n".format(self)
        for tracked_field in self.tracked_fields:
            res += (
                "dynamicforms.registerFieldAction('{ser.uuid}', '{tracked_field}', action_func{s.action_id});\n".format(
                    ser=serializer, tracked_field=tracked_field, s=self
                )
            )
        return res


class FormInitAction(ActionBase):
    def copy_and_resolve_reference(self, serializer: Serializer):
        return FormInitAction(self.name, serializer, action=self.action)

    def to_component_params(self, row_data, serializer):
        """
        generates a dict with parameters for component that is going to represent this action.
        none means don't render / activate this action on this row

        :param row_data:
        :param serializer:
        :return:
        """
        # perhaps this function is misnamed: it should be row_render_params, because only the row-level properties are
        #  processed
        return self.name, None

    def render(self, serializer: Serializer, **kwds):
        # we need window.setTimeout because at the time of form generation, the initial fields value collection
        # hasn't been done yet
        return "window.setTimeout(function() {{ {0.action_js} }}, 1);\n".format(self)


class FieldInitAction(FieldChangeAction):
    def to_component_params(self, row_data, serializer):
        """
        generates a dict with parameters for component that is going to represent this action.
        none means don't render / activate this action on this row

        :param row_data:
        :param serializer:
        :return:
        """
        # perhaps this function is misnamed: it should be row_render_params, because only the row-level properties are
        #  processed
        return self.name, None

    def copy_and_resolve_reference(self, serializer: Serializer):
        return FieldInitAction(self.tracked_fields, self.name, serializer)

    def render(self, serializer: Serializer, **kwds):
        # we need window.setTimeout because at the time of form generation, the initial fields value collection
        # hasn't been done yet
        return "window.setTimeout(function() {{ {0.action_js} }}, 1);;\n".format(self)


class FormPosition(IntEnum):
    FORM_HEADER = 1
    FORM_FOOTER = 2


class FormButtonAction(ActionBase, RenderableActionMixin):
    DEFAULT_LABELS = {
        FormButtonTypes.CANCEL: _("Cancel"),
        FormButtonTypes.SUBMIT: _("Save changes"),
        FormButtonTypes.CUSTOM: "Custom",  # intended to be translated by using code
    }

    def __init__(
        self,
        btn_type: FormButtonTypes,
        label: str = None,
        btn_classes: str = None,
        button_is_primary: bool = None,
        position: FormPosition = FormPosition.FORM_FOOTER,
        name: Union[str, None] = None,
        serializer: Serializer = None,
        icon: Union[str, None] = None,
        action=None,
        display_style=None,
    ):
        ActionBase.__init__(self, name, serializer, action=action)
        title = label
        label = label or FormButtonAction.DEFAULT_LABELS[btn_type or FormButtonTypes.CUSTOM]
        RenderableActionMixin.__init__(
            self, label, title, icon, btn_classes, display_style or self.def_display_style(form_button=btn_type)
        )
        self.uuid = uuid_module.uuid1()
        self.btn_type = btn_type
        self.position = position or FormPosition.FORM_FOOTER

        if button_is_primary is None:
            button_is_primary = btn_type == FormButtonTypes.SUBMIT
        self.button_is_primary = button_is_primary

        DF = DYNAMICFORMS
        self.btn_classes = btn_classes or (
            DF.form_button_classes
            + " "
            + (DF.form_button_classes_primary if button_is_primary else DF.form_button_classes_secondary)
            + " "
            + (DF.form_button_classes_cancel if btn_type == FormButtonTypes.CANCEL else "")
        )

    def to_component_params(self, row_data, serializer):
        """
        generates a dict with parameters for component that is going to represent this action.
        none means don't render / activate this action on this row

        :param row_data:
        :param serializer:
        :return:
        """
        # perhaps this function is misnamed: it should be row_render_params, because only the row-level properties are
        #  processed
        return self.name, None

    def as_component_def(self):
        res = dict(
            uuid=str(self.uuid),
            element_id=f"{self.name}-{self.serializer.uuid}",
            type=self.btn_type.name,
            position=self.position.name,
        )
        res.update(ActionBase.as_component_def(self))
        res.update(RenderableActionMixin.as_component_def(self))
        return res

    def copy_and_resolve_reference(self, serializer):
        return FormButtonAction(
            self.btn_type, self.label, self.btn_classes, self.button_is_primary, self.position, self.name, serializer
        )

    def render(self, serializer: Serializer, position: FormPosition = None, **kwds):
        if self.btn_type == FormButtonTypes.CANCEL and position == "form":
            return ""
        action_js = None  # TODO self.action_js
        button_name = ('name="btn-%s"' % self.name) if self.name else ""
        if isinstance(action_js, str):
            action_js = self.prepare_string(action_js)
            action_js = action_js.format(**locals())

        is_submit = self.btn_type != FormButtonTypes.SUBMIT or position == FormPosition.FORM_FOOTER
        button_type = "submit" if is_submit else "button"

        data_dismiss = 'data-dismiss="modal"' if self.btn_type == FormButtonTypes.CANCEL else ""
        if self.btn_type == FormButtonTypes.SUBMIT:
            button_id = "save-" + str(serializer.uuid)
        else:
            button_id = "formbutton-" + str(self.uuid)
        if (self.btn_type != FormButtonTypes.SUBMIT or position == "dialog") and action_js:
            button_js = (
                '<script type="text/javascript">'
                '  $("#{button_id}").on("click", function() {{'
                "    {action_js}"
                "  }});"
                "</script>"
            ).format(**locals())
        else:
            button_js = ""

        return self.prepare_string(
            '<button type="{button_type}" class="{self.btn_classes}" {data_dismiss} {button_name} id="{button_id}">'
            "{self.label}</button>{button_js}".format(**locals()),
            False,
        )


class Actions(object):
    def __init__(
        self, *args, add_default_crud: bool = False, add_default_filter: bool = False, add_form_buttons: bool = True
    ) -> None:
        super().__init__()
        if len(args) == 1 and args[0] is None:
            self.actions = []
            return

        self.actions: List[ActionBase] = list(args)
        if add_default_crud:
            self.actions.append(
                TableAction(
                    TablePosition.HEADER, _("Add"), title=_("Add new record"), name="add", icon="add-circle-outline"
                )
            )
            self.actions.append(
                TableAction(
                    TablePosition.ROW_CLICK, _("Edit"), title=_("Edit record"), name="edit", icon="pencil-outline"
                )
            )
            self.actions.append(
                TableAction(
                    TablePosition.ROW_END,
                    label=_("Delete"),
                    title=_("Delete record"),
                    name="delete",
                    icon="trash-outline",
                )
            )
            self.actions.append(TableAction(TablePosition.ROW_CLICK, _("Sort"), title=_("Sort by column"), name="sort"))
        if add_default_filter:
            self.actions.append(
                TableAction(
                    TablePosition.HEADER, label=_("Filter"), title=_("Filter"), name="filter", icon="search-outline"
                )
            )

        if add_form_buttons:
            self.actions.append(FormButtonAction(btn_type=FormButtonTypes.CANCEL, name="cancel"))
            self.actions.append(FormButtonAction(btn_type=FormButtonTypes.SUBMIT, name="submit"))

        self.actions.append(FieldChangeAction(None, "value_changed"))

    def get_resolved_copy(self, serializer) -> "Actions":
        """
        Returns a copy of declared actions bound to the serializer
        :param serializer: serializer the copy will be bound to
        :return:
        """
        if not isinstance(serializer, Serializer):
            return Actions(None)

        actions = [a.copy_and_resolve_reference(serializer) for a in self.actions]

        # move actions from Field to Serializer
        actions.extend(
            [
                a.copy_and_resolve_reference(serializer)
                for field in serializer.fields.values()
                for a in getattr(field, "actions", Actions(None)).actions_not_suppressed(serializer)
                if isinstance(a, FieldChangeAction)
            ]
        )

        return Actions(*actions, add_form_buttons=False)

    def render_field_onchange(self, serializer):
        """
        renders all field onchange actions needed for dynamicforms.registerFieldAction() function

        :return: the actions rendered as template string
        """
        res = ""
        for action in self.actions:
            if isinstance(action, FieldChangeAction) and not isinstance(action, FieldInitAction):
                res += action.render(serializer)
        return res

    def render_form_init(self, serializer):
        """
        renders the function which will analyse initial form data and hide appropriate fields

        :return: the actions rendered as template string
        """
        res = ""
        for action in self.actions:
            if isinstance(action, FormInitAction):
                res += action.render(serializer)
        return res

    def render_field_init(self, serializer, field_name: str):
        """
        renders function that will initialise the field being rendered

        :return: the actions rendered as template string
        """
        res = ""
        for action in self.actions:
            if isinstance(action, FieldInitAction) and field_name in action.tracked_fields:
                res += action.render(serializer)
        return res

    def renderable_actions(self, serializer: Serializer):
        request = serializer.context.get("request", None)
        viewset = serializer.context.get("view", None)
        return (
            a
            for a in self.actions
            if isinstance(a, TableAction) and not serializer.suppress_action(a, request, viewset)
        )

    def render_renderable_actions(
        self, allowed_positions: Iterable[TablePosition], field_name: str, serializer: Serializer
    ):
        """
        Returns those actions that are not suppressed
        :return: List[Action]
        """
        res = ""

        for action in self.renderable_actions(serializer):
            if action.position in allowed_positions and (field_name is None or field_name == action.field_name):
                res += action.render(serializer)
        return res

    def actions_not_suppressed(self, serializer: Serializer):
        request = serializer.context.get("request", None)
        viewset = serializer.context.get("view", None)

        return (a for a in self.actions if not serializer.suppress_action(a, request, viewset))

    def render_form_buttons(self, serializer: Serializer, position: str):
        """
        Renders form buttons
        :return: List[Action]
        """
        request = serializer.context.get("request", None)
        viewset = serializer.context.get("view", None)

        res = ""

        for button in self.actions:
            if (
                isinstance(button, FormButtonAction)
                and position == button.position
                and not serializer.suppress_action(button, request, viewset)
            ):
                res += button.render(serializer, position=position)
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
