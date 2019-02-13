from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from dynamicforms import serializers, viewsets, fields
from dynamicforms.buttons import FormButtons, Button, FormButtonTypes


class SingleDialogSerializer(serializers.Serializer):
    form_titles = {
        'table': '',
        'new': 'Choose a value',
        'edit': '',
    }
    form_template = 'examples/single_dialog.html'

    test = fields.ChoiceField(label='What should we say?', choices=(
        ('Today is sunny', 'Today is sunny'),
        ('Never-ending rain', 'Never-ending rain')
    ))

    form_buttons = FormButtons([
        Button(btn_type=FormButtonTypes.CUSTOM, label='Confirm', js="customSingleDialogBtn();")
    ])


class SingleDialogViewSet(viewsets.SingleRecordViewSet):
    serializer_class = SingleDialogSerializer

    template_context = dict(url_reverse='single-dialog', dialog_classes='modal-lg', dialog_header_classes='bg-info')

    def new_object(self):
        return dict(test=None)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # return Response(, content_type='application/json')
        return HttpResponse(JSONRenderer().render(serializer.data))
