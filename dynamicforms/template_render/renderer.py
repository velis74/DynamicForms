from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from dynamicforms.settings import DYNAMICFORMS


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
        request = view.request
        render_type = request.META.get('HTTP_X_DF_RENDER_TYPE', request.GET.get('df_render_type', 'page'))
        if render_type == 'page':
            return [DYNAMICFORMS.page_template]
        elif render_type == 'dialog':
            response['Content-Type'] = 'application/json'  # response.accepted_media_type and .content_type don't work
            return ['template_render/render_dialog.json']
        else:
            raise NotImplementedError(f'ComponentHTMLRenderer doesn\'t know how to render {render_type}')
        # return super().get_template_names(response, view)

    def get_template_context(self, data, renderer_context):
        if isinstance(data, dict) and 'next' in data and 'results' in data and \
                isinstance(data['results'], (ReturnList, ReturnDict)):
            return dict(serializer=data['results'].serializer)
        if isinstance(data, (ReturnList, ReturnDict)):
            return dict(serializer=data.serializer)
        return super().get_template_context(data, renderer_context)
