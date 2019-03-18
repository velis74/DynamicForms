import six
from django.template import loader
from rest_framework.renderers import HTMLFormRenderer, TemplateHTMLRenderer
from rest_framework.serializers import HiddenField, ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from .settings import DYNAMICFORMS


# noinspection PyRedeclaration
class TemplateHTMLRenderer(TemplateHTMLRenderer):
    """
    Renderers serializer data into an HTML form.

    If the serializer was instantiated without an object then this will
    return an HTML form not bound to any object,
    otherwise it will return an HTML form with the appropriate initial data
    populated from the object.

    Note that rendering of field and form errors is not currently supported.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        link_next = link_prev = ''

        if isinstance(data, dict) and 'next' in data and 'results' in data and \
                isinstance(data['results'], (ReturnList, ReturnDict)):
            # This is in case of Pagination
            link_next = data.get('next', '')
            link_prev = data.get('previous', '')
            data = data['results']
        if isinstance(data, (ReturnList, ReturnDict)):
            ser = data.serializer
            data = dict(data=data, serializer=ser.child if isinstance(ser, ListSerializer) else ser,
                        link_next=link_next, link_prev=link_prev)

            if getattr(ser, '_errors', {}):
                # CAUTION: bad hacks start here. This should be removed at some point

                # unmark exception from response because this was a validation error
                # This will allow TemplateHTMLRenderer to still render the template as if it was without problems
                # If this is not done, the only result user will see will be a 404 error without any details
                response = renderer_context['response']
                response.exception = False

                # result data should be object data otherwise nothing will render...
                data['data'] = data['serializer'].data

        return super().render(data, accepted_media_type, renderer_context)

    def get_template_names(self, response, view):
        if view.render_type == 'page' and DYNAMICFORMS.page_template:
            return [DYNAMICFORMS.page_template]
        return super().get_template_names(response, view)

    def get_template_context(self, data, renderer_context):
        res = super().get_template_context(data, renderer_context)
        view = renderer_context['view']
        if hasattr(view, 'template_context'):
            if callable(view.template_context):
                res.update(view.template_context())
            else:
                res.update(view.template_context)
        res['df_render_type'] = view.render_type  # This one should not fail because it's set in initialize_request
        res['DYNAMICFORMS'] = DYNAMICFORMS
        return res


# noinspection PyRedeclaration
class HTMLFormRenderer(HTMLFormRenderer):
    """
    An HTML renderer for use with templates.

    The data supplied to the Response object should be a dictionary that will
    be used as context for the template.

    The template name is determined by (in order of preference):

    1. An explicit `.template_name` attribute set on the response.
    2. An explicit `.template_name` attribute set on this class.
    3. The return result of calling `view.get_template_names()`.

    For example:
        data = {'users': User.objects.all()}
        return Response(data, template_name='users.html')
    """

    def render_field(self, field, parent_style):
        # noinspection PyProtectedMember
        if isinstance(field._field, HiddenField):
            return ''

        style = dict(self.default_style[field])
        style.update(field.style)
        if 'template_pack' not in style:
            style['template_pack'] = parent_style.get('template_pack', self.template_pack)
        style['serializer'] = parent_style.get('serializer', None)
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
            'DYNAMICFORMS': DYNAMICFORMS,
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
        style['template_pack'] = DYNAMICFORMS.template + 'field'
        style['renderer'] = self

        template_pack = style['template_pack'].strip('/')

        # getting the template to use
        template_name = next((x for x in (  # Get the first specified template name as encountered
            style.get('form_template', None),  # template name from tag parameter
            getattr(self, 'form_template', None),  # if ViewSet set the form_template member of this renderer
            getattr(form, 'form_template', None),  # if Serializer has form_template member set
            template_pack + '/' + self.base_template  # take default template from pack
        ) if x))

        template = loader.get_template(template_name)
        context = {
            'form': form,
            'style': style,
            'DYNAMICFORMS': DYNAMICFORMS,
        }
        return template.render(context)
