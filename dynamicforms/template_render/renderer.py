from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class ComponentHTMLRenderer(TemplateHTMLRenderer):
    media_type = 'text/html'
    format = 'component'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return super().render(data, accepted_media_type, renderer_context)

    def get_template_names(self, response, view):
        return ['examples/view_mode.html']
        # return super().get_template_names(response, view)

    def get_template_context(self, data, renderer_context):
        if isinstance(data, dict) and 'next' in data and 'results' in data and \
                isinstance(data['results'], (ReturnList, ReturnDict)):
            return dict(page_data=data['results'].serializer)
        if isinstance(data, (ReturnList, ReturnDict)):
            return dict(page_data=data.serializer)
        return super().get_template_context(data, renderer_context)
