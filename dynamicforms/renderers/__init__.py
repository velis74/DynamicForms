import six
from .. import settings
from django.template import loader
from rest_framework.serializers import ListSerializer, HiddenField
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
        res['df_dialog'] = getattr(view, 'render_to_dialog', False)

        res['DF'] = settings.CONTEXT_VARS
        return res


# noinspection PyRedeclaration
class HTMLFormRenderer(HTMLFormRenderer):

    def render_field(self, field, parent_style):
        if isinstance(field._field, HiddenField):
            return ''

        style = dict(self.default_style[field])
        style.update(field.style)
        if 'template_pack' not in style:
            style['template_pack'] = parent_style.get('template_pack', self.template_pack)
        style['renderer'] = self

        # Get a clone of the field with text-only value representation.
        field = field.as_form_field()

        if style.get('input_type') == 'datetime-local' and isinstance(field.value, six.text_type):
            field.value = field.value.rstrip('Z')

        if 'template' in style:
            template_name = style['template']
        else:
            template_name = style['template_pack'].strip('/') + '/' + style['base_template']

        template = loader.get_template(template_name)
        context = {
            'field': field,
            'style': style,
            'DF': settings.CONTEXT_VARS,
        }
        return template.render(context)

    # Jure: had to copy this one over to support custom template as parameter + DF context variable
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

        # getting the template to use
        template_name = next((x for x in (  # Get the first specified template name as encountered
            renderer_context.get('form_template', None),  # template name from tag parameter
            getattr(self, 'form_template', None),  # if ViewSet set the form_template member of this renderer
            getattr(form, 'form_template', None),  # if Serializer has form_template member set
            template_pack + '/' + self.base_template  # take default template from pack
        ) if x))

        template = loader.get_template(template_name)
        context = {
            'form': form,
            'style': style,
            'DF': settings.CONTEXT_VARS,
        }
        return template.render(context)
