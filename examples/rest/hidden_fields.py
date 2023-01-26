from dynamicforms_legacy import serializers
from dynamicforms_legacy.action import Actions, FieldChangeAction, FormInitAction
from dynamicforms_legacy.viewsets import ModelViewSet
from ..models import HiddenFields


class HiddenFieldsSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Hidden fields list',
        'new': 'New hidden fields object',
        'edit': 'Editing hidden fields object',
    }

    actions = Actions(
        FieldChangeAction(['note'], 'examples.action_hiddenfields_note'),
        FieldChangeAction(['unit'], 'examples.action_hiddenfields_unit'),
        FormInitAction('examples.hide_fields_on_show("{{ serializer.uuid }}");'),
        add_default_crud=True, add_default_filter=False
    )

    class Meta:
        model = HiddenFields
        exclude = ()


class HiddenFieldsViewSet(ModelViewSet):
    template_context = dict(url_reverse='hidden-fields')

    queryset = HiddenFields.objects.all()
    serializer_class = HiddenFieldsSerializer
