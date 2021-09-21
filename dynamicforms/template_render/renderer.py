from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from dynamicforms.settings import DYNAMICFORMS


class ComponentDefRenderer(JSONRenderer):
    format = 'componentdef'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        serializer = None

        if isinstance(data, dict) and 'next' in data and 'results' in data and \
            isinstance(data['results'], (ReturnList, ReturnDict)):
            serializer = data['results'].serializer
        if isinstance(data, (ReturnList, ReturnDict)):
            serializer = data.serializer

        assert serializer is not None

        serializer.apply_component_context()
        return super().render(serializer.component_params(output_json=False), accepted_media_type, renderer_context)


class ComponentHTMLRenderer(TemplateHTMLRenderer):
    media_type = 'text/html'
    format = 'component'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        DYNAMICFORMS.components = True
        try:
            return super().render(data, accepted_media_type, renderer_context)
        finally:
            DYNAMICFORMS.components = False

    def get_template_names(self, response, view):
        return [DYNAMICFORMS.page_template]

    def get_template_context(self, data, renderer_context):
        if isinstance(data, dict) and 'next' in data and 'results' in data and \
            isinstance(data['results'], (ReturnList, ReturnDict)):
            return dict(serializer=data['results'].serializer)
        if isinstance(data, (ReturnList, ReturnDict)):
            return dict(serializer=data.serializer)
        return super().get_template_context(data, renderer_context)
