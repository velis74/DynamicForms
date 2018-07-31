from rest_framework import viewsets
from rest_framework.response import Response
from django.http import Http404


class NewMixin(object):

    def new_object(self: viewsets.ModelViewSet):
        self.get_queryset().model()

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
