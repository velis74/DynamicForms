from rest_framework import viewsets
from rest_framework.response import Response
from django.http import Http404
from ..renderers import TemplateHTMLRenderer
from ..settings import BSVER_MODAL


class NewMixin(object):
    """
    Provides support for retrieving default values for a new record
    """

    def new_object(self: viewsets.ModelViewSet):
        # TODO: Tukaj moraš paziti, da je objekt pravilno postavljen glede na pravila
        # Primer: če se plačnik nastavi iz pilota in tukaj prednapolniš pilota, potem poskrbi, da boš prednapolnil
        # tudi plačnika.
        #
        # Kako pa to lahko naredimo?
        # Predlog: retrieve, ko pokliče to funkcijo, naj tudi izvede "onchange" event za vsako polje in tako to napolni
        return self.get_queryset().model()

    # noinspection PyUnresolvedReferences
    def retrieve(self: viewsets.ModelViewSet, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            if filter_kwargs.get('pk', None) == 'new':
                instance = self.new_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise


class ModelViewSet(NewMixin, viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        # this relies on TemplateHTMLRenderer.get_template_names which first checks for template declared in Response
        if hasattr(self, 'list_template_name'):
            res.template_name = self.list_template_name
        return res

    def initialize_request(self, request, *args, **kwargs):
        # Caution: just to be sure for any future debugging: the request parameter to this function is a WSGIRequest
        #  while the return Request is actually DRF Request
        #  As a consequence, form values don't get parsed until you actually call super().initialize_request
        #  There's no "request.data", etc. Just saying. So you don't debug for two hours next time. By "you" I mean me

        # noinspection PyAttributeOutsideInit
        self.render_to_dialog = request.META.get('X-DF-DIALOG', request.GET.get('df_dialog', False))

        if request.method.lower() == 'post' and request.POST.get('data-dynamicforms-method', None):
            # This is a hack because HTML forms can only do POST & GET. This way we also get PUT & PATCH
            request.method = request.POST.get('data-dynamicforms-method')
        return super().initialize_request(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        res = super().finalize_response(request, response, *args, **kwargs)
        if self.render_to_dialog and isinstance(res.accepted_renderer, TemplateHTMLRenderer):
            res.template_name = BSVER_MODAL
        return res
