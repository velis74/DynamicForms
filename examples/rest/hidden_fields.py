from dynamicforms import serializers
from dynamicforms.mixins import Action
from dynamicforms.viewsets import ModelViewSet
from ..models import HiddenFields


class HiddenFieldsSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Hidden fields list',
        'new': 'New hidden fields object',
        'edit': 'Editing hidden fields object',
    }

    # TODO: skrij samo unit, potem pa pošlji onchanged njemu in naj on skrije še ostala polja
    # TODO: ko pa unit spet pokažeš, spet pošlješ zadevo njemu in on bo pogledal, katero od polj mora pokazati
    actions = [
        Action(['note'], 'examples.action_hiddenfields_note'),
        Action(['unit'], 'examples.action_hiddenfields_unit'),
    ]

    class Meta:
        model = HiddenFields
        exclude = ()


class HiddenFieldsViewSet(ModelViewSet):
    template_context = dict(url_reverse='hidden-fields')

    queryset = HiddenFields.objects.all()
    serializer_class = HiddenFieldsSerializer
