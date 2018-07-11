from rest_framework.serializers import ListSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.utils.serializer_helpers import ReturnList


# noinspection PyRedeclaration
class TemplateHTMLRenderer(TemplateHTMLRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            ser = data.serializer
            data = dict(data=data, serializer=ser.child if isinstance(ser, ListSerializer) else ser)
        return super().render(data, accepted_media_type, renderer_context)

    def get_template_context(self, data, renderer_context):
        res = super().get_template_context(data, renderer_context)
        view = renderer_context['view']
        if hasattr(view, 'template_context'):
            res.update(view.template_context)
        return res
