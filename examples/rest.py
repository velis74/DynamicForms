from django.utils.safestring import mark_safe

from dynamicforms import serializers
from dynamicforms.mixins import Action
from dynamicforms.viewsets import ModelViewSet
from rest_framework import routers
from rest_framework.exceptions import ValidationError
from .models import Validated, HiddenFields


# TODO: templates/examples/validated* je treba prenest v dynamicforms/templates (standardni templati morajo bit pokrit)


class ValidatedSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Validated list',
        'new': 'New validated object',
        'edit': 'Editing validated object',
    }

    # id = serializers.IntegerField(required=False)  # so that it shows at all

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['amount'] != 5:
            if attrs['code'] != '123':
                raise ValidationError({'amount': 'amount can only be different than 5 if code is "123"'})

        if attrs['enabled'] is True and attrs['item_type'] == 3:
            raise ValidationError('When enabled you can only choose from first three item types')

        return attrs

    class Meta:
        model = Validated
        exclude = ()


class ValidatedViewSet(ModelViewSet):
    # renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'examples/model_single.html'
    template_name_list = 'examples/model_list.html'
    template_context = dict(url_reverse='validated')

    queryset = Validated.objects.all()
    serializer_class = ValidatedSerializer


class HiddenFieldsSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Hidden fields list',
        'new': 'New hidden fields object',
        'edit': 'Editing hidden fields object',
    }

    # TODO: skrij samo unit, potem pa pošlji onchanged njemu in naj on skrije še ostala polja
    # TODO: ko pa unit spet pokažeš, spet pošlješ zadevo njemu in on bo pogledal, katero od polj mora pokazati
    actions = [
        Action(['note'], mark_safe('examples.action_hiddenfields_note')),
        Action(['unit'], mark_safe('examples.action_hiddenfields_unit')),
    ]

    class Meta:
        model = HiddenFields
        exclude = ()


class HiddenFieldsViewSet(ModelViewSet):
    template_name = 'examples/model_single.html'
    template_name_list = 'examples/model_list.html'
    template_context = dict(url_reverse='hidden-fields')

    queryset = HiddenFields.objects.all()
    serializer_class = HiddenFieldsSerializer


router = routers.DefaultRouter()
router.register(r'validated', ValidatedViewSet, base_name='validated')
router.register(r'hidden-fields', HiddenFieldsViewSet, base_name='hidden-fields')
