from dynamicforms import serializers
from dynamicforms.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from ..models import Validated


class ValidatedSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Validated list',
        'new': 'New validated object',
        'edit': 'Editing validated object',
    }

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
    template_context = dict(url_reverse='validated')

    queryset = Validated.objects.all()
    serializer_class = ValidatedSerializer
