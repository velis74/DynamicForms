import time

from django.http.response import HttpResponse
from rest_framework.renderers import JSONRenderer

from dynamicforms import fields, serializers, viewsets
from dynamicforms.action import Actions, FormButtonAction, FormButtonTypes
from dynamicforms.progress import get_progress_key, set_progress_comment, set_progress_value


class SingleDialogSerializer(serializers.Serializer):
    template_context = dict(url_reverse='single-dialog', dialog_classes='modal-lg', dialog_header_classes='bg-info')
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
        FormButtonAction(FormButtonTypes.CANCEL, name='cancel'),
        FormButtonAction(FormButtonTypes.CUSTOM, name='download', label='Download it'),
        FormButtonAction(FormButtonTypes.CUSTOM, name='say_it', label='Say it', button_is_primary=True),
        add_form_buttons=False
    )


class SingleDialogViewSet(viewsets.SingleRecordViewSet):
    serializer_class = SingleDialogSerializer

    def new_object(self):
        return dict(test=None)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.data.get('download', '') == '1':
            res = HttpResponse(serializer.data['test'].encode('utf-8'), content_type='text/plain; charset=UTF-8')
            res['Content-Disposition'] = 'attachment; filename={}'.format('justsaying.txt')
            return res

        progress_key = get_progress_key(request)
        for i in range(10):
            set_progress_comment(progress_key, 'Processing #%d' % (i + 1))
            set_progress_value(progress_key, (i + 1) * 10)
            time.sleep(0.5)

        return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')
