from dynamicforms import fields, serializers
from dynamicforms.mixins import DisplayMode
from dynamicforms.viewsets import ModelViewSet
from examples.models import AdvancedFields


class WriteOnlyFieldsSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse="write-only-fields")
    form_titles = {
        "table": "Write only fields list",
        "new": "New write only fields object",
        "edit": "Editing write only fields object",
    }

    regex_field = fields.CharField(label="Hidden", write_only=True)
    choice_field = fields.CharField(label="Shown", write_only=True, display=DisplayMode.FULL)

    class Meta:
        model = AdvancedFields
        fields = ("id", "regex_field", "choice_field")


class WriteOnlyFieldsViewSet(ModelViewSet):
    pagination_class = ModelViewSet.generate_paged_loader(30)

    queryset = AdvancedFields.objects.all()
    serializer_class = WriteOnlyFieldsSerializer
