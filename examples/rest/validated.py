from rest_framework.exceptions import ValidationError

from dynamicforms import fields, serializers
from dynamicforms.action import Actions
from dynamicforms.viewsets import ModelViewSet

from ..models import Validated


class ValidatedSerializer(serializers.ModelSerializer):
    """
    Example showing field validation, both at the field level and at the record level
    """

    template_context = dict(url_reverse="validated")
    form_titles = {
        "table": "Validated list",
        "new": "New validated object",
        "edit": "Editing validated object",
    }
    actions = Actions(add_default_crud=True, add_default_filter=False, add_form_buttons=True)

    item_type = fields.ChoiceField(choices=Validated.ItemTypeChoices.get_df_tuple())

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs["amount"] != 5:
            if attrs["code"] != "123":
                raise ValidationError({"amount": 'amount can only be different than 5 if code is "123"'})

        if attrs["enabled"] is True and attrs["item_type"] == 3:
            raise ValidationError("When enabled you can only choose from first three item types")

        return attrs

    class Meta:
        model = Validated
        exclude = ()


class ValidatedViewSet(ModelViewSet):
    queryset = Validated.objects.all()
    serializer_class = ValidatedSerializer
