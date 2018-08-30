from rest_framework import routers
from rest_framework.exceptions import ValidationError
from dynamicforms.viewsets import ModelViewSet
from dynamicforms import serializers
from .models import Validated


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

        # TODO: tegale spodaj naredi, da bo odletel samo ob določenem brez veznem (ampak common-case) pogoju
        # noinspection PyUnreachableCode
        if False:
            raise ValidationError('I\'m just messing with you, you will NEVER get this form validated')

        return attrs

    class Meta:
        model = Validated
        exclude = ()


class ValidatedViewSet(ModelViewSet):
    # renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'examples/validated.html'
    list_template_name = 'examples/validated_list.html'
    template_context = dict(crud_form=True, url_reverse='validated')

    queryset = Validated.objects.all()
    serializer_class = ValidatedSerializer


router = routers.DefaultRouter()
router.register(r'rest/validated', ValidatedViewSet, base_name='validated')
# router.register(r'rest/hidden-fields', HiddenFieldsViewSet, base_name='hidden_fields')
