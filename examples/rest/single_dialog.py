from dynamicforms import serializers, viewsets, fields
from ..models import Relation


class SingleDialogSerializer(serializers.Serializer):
    form_titles = {
        'table': '',
        'new': 'Show single record',
        'edit': '',
    }
    form_template = 'examples/single_dialog.html'

    test = fields.ChoiceField(choices=(
        (1, 'Test 1'),
        (2, 'Test 2')
    ))

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class SingleDialogViewSet(viewsets.SingleRecordViewSet):
    serializer_class = SingleDialogSerializer

    template_context = dict(url_reverse='single-dialog', dialog_classes='modal-lg', dialog_header_classes='bg-info')

    def new_object(self):
        return dict(test=None)
