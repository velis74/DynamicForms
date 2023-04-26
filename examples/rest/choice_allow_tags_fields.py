from dynamicforms import fields, serializers
from dynamicforms.mixins import DisplayMode
from dynamicforms.viewsets import ModelViewSet
from examples.models import AdvancedFields


class ChoiceAllowTagsFieldsSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse="choice-allow-tags-fields")
    form_titles = {
        "table": "Choices allow tags list",
        "new": "New Choices allow tags fields object",
        "edit": "Editing Choices allow tags fields object",
    }

    choice_field = fields.ChoiceField(
        label="Choice",
        display=DisplayMode.FULL,
        allow_tags=True,
        choices=(("0", "Choice 1"), ("1", "Choice 2"), ("2", "Choice 3"), ("3", "Choice 4")),
    )

    multiplechoice_field = fields.MultipleChoiceField(
        label="Multiple choice",
        display=DisplayMode.FULL,
        allow_tags=True,
        choices=(
            ("0", "Multiple choice 1"),
            ("1", "Multiple choice 2"),
            ("2", "Multiple choice 3"),
            ("3", "Multiple choice 4"),
        ),
    )

    class Meta:
        model = AdvancedFields
        fields = ("id", "choice_field", "multiplechoice_field")


class ChoiceAllowTagsFieldsViewSet(ModelViewSet):
    pagination_class = ModelViewSet.generate_paged_loader(30)

    queryset = AdvancedFields.objects.all()
    serializer_class = ChoiceAllowTagsFieldsSerializer
