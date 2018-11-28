from dynamicforms import serializers
from dynamicforms.viewsets import ModelViewSet
from ..models import PageLoad


# TODO: templates/examples/validated* je treba prenest v dynamicforms/templates (standardni templati morajo bit pokrit)


class PageLoadSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Dynamic page loader list',
        'new': 'New object',
        'edit': 'Editing object',
    }

    class Meta:
        model = PageLoad
        exclude = ()


class PageLoadViewSet(ModelViewSet):
    template_name = 'dynamicforms/bootstrap/base_list.html'
    template_context = dict(url_reverse='page-load')
    pagination_class = ModelViewSet.generate_paged_loader(30)

    queryset = PageLoad.objects.all()
    serializer_class = PageLoadSerializer
