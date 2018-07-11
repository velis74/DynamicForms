from rest_framework import viewsets


class ModelViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        # this relies on TemplateHTMLRenderer.get_template_names which first checks for template declared in Response
        if hasattr(self, 'list_template_name'):
            res.template_name = self.list_template_name
        return res
