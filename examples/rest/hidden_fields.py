from dynamicforms import serializers
from dynamicforms.action import Actions, FieldChangeAction, FormInitAction
from dynamicforms.viewsets import ModelViewSet
from ..models import HiddenFields


class HiddenFieldsSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse='hidden-fields')
    component_name = 'ExampleHiddenLayout'
    form_titles = {
        'table': 'Hidden fields list',
        'new': 'New hidden fields object',
        'edit': 'Editing hidden fields object',
    }

    actions = Actions(
        FieldChangeAction(['note'], 'examples.action_hiddenfields_note', name='field_note_change'),
        FieldChangeAction(['unit'], 'examples.action_hiddenfields_unit', name='field_unit_change'),
        FormInitAction('examples.hide_fields_on_show("{{ serializer.uuid }}");', name='form_init'),
        add_default_crud=True, add_default_filter=False
    )

    class Meta:
        model = HiddenFields
        exclude = ()


class HiddenFieldsViewSet(ModelViewSet):
    queryset = HiddenFields.objects.all()
    serializer_class = HiddenFieldsSerializer
