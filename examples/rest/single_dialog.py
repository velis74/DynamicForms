from django.http.response import HttpResponse
from rest_framework.renderers import JSONRenderer

from dynamicforms import fields, serializers, viewsets
from dynamicforms.action import Actions, FormButtonAction, FormButtonTypes


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

    actions = Actions(
        FormButtonAction(FormButtonTypes.CANCEL),
        FormButtonAction(FormButtonTypes.CUSTOM, label='Download it', action_js="customSingleDialogBtnPost();"),
        FormButtonAction(FormButtonTypes.CUSTOM, label='Say it', button_is_primary=True,
                         action_js="customSingleDialogBtn();"),
        add_form_buttons=False
    )


class SingleDialogViewSet(viewsets.SingleRecordViewSet):
    serializer_class = SingleDialogSerializer

    template_context = dict(url_reverse='single-dialog', dialog_classes='modal-lg', dialog_header_classes='bg-info')

    def new_object(self):
        return dict(test=None)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.data.get('download', '') == '1':
            res = HttpResponse(serializer.data['test'].encode('utf-8'), content_type='text/plain; charset=UTF-8')
            res['Content-Disposition'] = 'attachment; filename={}'.format('justsaying.txt')
            return res

        return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')
