from dynamicforms import serializers
from dynamicforms.action import Actions, FieldChangeAction, FormInitAction, TableAction, TablePosition
from dynamicforms.viewsets import ModelViewSet

from ..models import HiddenFields


class ActionsOverviewSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse="actions-overview")
    form_titles = {
        "table": "Actions overview list",
        "new": "New actions overview object",
        "edit": "Editing actions overview object",
    }

    actions = Actions(
        TableAction(
            position=TablePosition.FIELD_START,
            label="Up",
            name="up",
            icon="arrow-up-circle-outline",
            field_name="note",
            display_style=dict(
                md=dict(asButton=False, showIcon=True, showLabel=True),
                xs=dict(asButton=False, showIcon=True, showLabel=False),
                xl=dict(asButton=True, showIcon=True, showLabel=True),
            ),
        ),
        TableAction(
            position=TablePosition.FIELD_START,
            label="Up",
            name="up-unit",
            icon="arrow-up-circle-outline",
            field_name="unit",
            display_style=dict(
                xs=dict(showIcon=True),
                sm=dict(showIcon=False),
                md=dict(showIcon=True),
                lg=dict(showIcon=False),
                xl=dict(showIcon=True),
            ),
        ),
        TableAction(
            position=TablePosition.FIELD_START,
            label="Up",
            name="up-int_fld",
            icon="arrow-up-circle-outline",
            field_name="int_fld",
            display_style=dict(
                sm=dict(showIcon=False),
                lg=dict(showIcon=True, showLabel=False),
            ),
        ),
        TableAction(
            position=TablePosition.FIELD_END,
            label="Down",
            name="down",
            icon="arrow-down-circle-outline",
            field_name="cst_fld",
            display_style=dict(
                asButton=False,
                showIcon=True,
                showLabel=False,
            ),
        ),
        TableAction(
            position=TablePosition.ROW_END,
            label="Edit",
            name="Edit",
            icon="pencil-outline",
            display_style=dict(
                asButton=True,
                showIcon=True,
                showLabel=True,
            ),
        ),
        FieldChangeAction(["note"], name="field_note_change"),  # TODO action_js='examples.action_hiddenfields_note',
        FieldChangeAction(["unit"], name="field_unit_change"),  # TODO action_js='examples.action_hiddenfields_unit'
        FormInitAction(name="form_init"),  # TODO: action_js: 'examples.hide_fields_on_show("{{ serializer.uuid }}");'
        add_default_crud=True,
        add_default_filter=False,
    )

    class Meta:
        model = HiddenFields
        exclude = ()


class ActionsOverviewViewSet(ModelViewSet):
    queryset = HiddenFields.objects.all()
    serializer_class = ActionsOverviewSerializer
