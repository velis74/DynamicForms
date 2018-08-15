from .. import settings
from django.template import loader
from rest_framework.serializers import ListSerializer
from rest_framework.renderers import TemplateHTMLRenderer, HTMLFormRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict


# noinspection PyRedeclaration
class TemplateHTMLRenderer(TemplateHTMLRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, (ReturnList, ReturnDict)):
            ser = data.serializer
            data = dict(data=data, serializer=ser.child if isinstance(ser, ListSerializer) else ser)

            if getattr(ser, '_errors', {}):
                # unmark exception from response because this was a validation error
                # This will allow TemplateHTMLRenderer to still render the template as if it was without problems
                # If this is not done, the only result user will see will be a 404 error without any details
                response = renderer_context['response']
                response.exception = False

        return super().render(data, accepted_media_type, renderer_context)

    def get_template_context(self, data, renderer_context):
        res = super().get_template_context(data, renderer_context)
        view = renderer_context['view']
        if hasattr(view, 'template_context'):
            res.update(view.template_context)

        res['DF'] = settings.CONTEXT_VARS
        return res


# noinspection PyRedeclaration
class HTMLFormRenderer(HTMLFormRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render serializer data and return an HTML form, as a string.
        """
        renderer_context = renderer_context or {}
        form = data.serializer

        style = renderer_context.get('style', {})
        if 'template_pack' not in style:
            style['template_pack'] = self.template_pack
        style['renderer'] = self

        template_pack = style['template_pack'].strip('/')

        # take a specific form template (if specified) or get it from template pack
        template_name = renderer_context.get('form_template', template_pack + '/' + self.base_template)
        template = loader.get_template(template_name)
        context = {
            'form': form,
            'style': style
        }
        return template.render(context)
