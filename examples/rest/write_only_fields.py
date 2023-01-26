from dynamicforms_legacy import fields, serializers
from dynamicforms_legacy.mixins import DisplayMode
from dynamicforms_legacy.viewsets import ModelViewSet
from examples.models import AdvancedFields


class WriteOnlyFieldsSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Write only fields list',
        'new': 'New write only fields object',
        'edit': 'Editing write only fields object',
    }

    regex_field = fields.CharField(label='Hidden', write_only=True)
    choice_field = fields.CharField(label='Shown', write_only=True, display=DisplayMode.FULL)

    class Meta:
        model = AdvancedFields
        fields = ('id', 'regex_field', 'choice_field')


class WriteOnlyFieldsViewSet(ModelViewSet):
    template_context = dict(url_reverse='write-only-fields')
    pagination_class = ModelViewSet.generate_paged_loader(30)

    queryset = AdvancedFields.objects.all()
    serializer_class = WriteOnlyFieldsSerializer
