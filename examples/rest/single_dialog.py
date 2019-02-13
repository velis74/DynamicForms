from django.utils.translation import ugettext_lazy as _
from dynamicforms import serializers, viewsets, fields
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http.response import HttpResponse


class SingleDialogSerializer(serializers.Serializer):
    form_titles = {
        'table': '',
        'new': 'Choose a value',
        'edit': '',
    }
    form_template = 'examples/single_dialog.html'

    test = fields.ChoiceField(label=_('What should we say?'), choices=(
        (1, 'Today is sunny'),
        (2, 'Never-ending rain')
    ))

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class SingleDialogViewSet(viewsets.SingleRecordViewSet):
    serializer_class = SingleDialogSerializer

    template_context = dict(url_reverse='single-dialog', dialog_classes='modal', dialog_header_classes='bg-info')

    def new_object(self):
        return dict(test=None)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # return Response(, content_type='application/json')
        return HttpResponse(JSONRenderer().render(serializer.data))
