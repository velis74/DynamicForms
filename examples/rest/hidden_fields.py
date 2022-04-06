from dynamicforms import serializers
from dynamicforms.action import Actions, FieldChangeAction, FormInitAction, TableAction, TablePosition
from dynamicforms.template_render.layout import Layout
from dynamicforms.viewsets import ModelViewSet
from ..models import HiddenFields


class HiddenFieldsSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse='hidden-fields')
    form_titles = {
        'table': 'Hidden fields list',
        'new': 'New hidden fields object',
        'edit': 'Editing hidden fields object',
    }

    actions = Actions(
        TableAction(position=TablePosition.FIELD_START, label="Up", action_js='', name='up',
                    icon='arrow-up-circle-outline', field_name="note",
                    display_style=dict(md=dict(asButton=False, showIcon=True, showLabel=True),
                                       xs=dict(asButton=False, showIcon=True, showLabel=False),
                                       xl=dict(asButton=True, showIcon=True, showLabel=True))),
        TableAction(position=TablePosition.FIELD_START, label="Up", action_js='', name='up-unit',
                    icon='arrow-up-circle-outline', field_name="unit",
                    display_style=dict(xs=dict(showIcon=True),
                                       sm=dict(showIcon=False),
                                       md=dict(showIcon=True),
                                       lg=dict(showIcon=False),
                                       xl=dict(showIcon=True))),
        TableAction(position=TablePosition.FIELD_START, label="Up", action_js='', name='up-int_fld',
                    icon='arrow-up-circle-outline', field_name="int_fld",
                    display_style=dict(sm=dict(showIcon=False),
                                       lg=dict(showIcon=True, showLabel=False),
                                       )),
        TableAction(position=TablePosition.FIELD_END, label="Down", action_js='', name='down',
                    icon='arrow-down-circle-outline', field_name="cst_fld",
                    display_style=dict(asButton=False, showIcon=True, showLabel=False, )),
        TableAction(position=TablePosition.ROW_END, label="Edit", action_js='', name='Edit',
                    icon='pencil-outline',
                    display_style=dict(asButton=True, showIcon=True, showLabel=True, )),
        FieldChangeAction(['note'], 'examples.action_hiddenfields_note', name='field_note_change'),
        FieldChangeAction(['unit'], 'examples.action_hiddenfields_unit', name='field_unit_change'),
        FormInitAction('examples.hide_fields_on_show("{{ serializer.uuid }}");', name='form_init'),
        add_default_crud=True, add_default_filter=False
    )

    class Meta:
        model = HiddenFields
        exclude = ()
        layout = Layout('ExampleHiddenLayout')


class HiddenFieldsViewSet(ModelViewSet):
    queryset = HiddenFields.objects.all()
    serializer_class = HiddenFieldsSerializer
