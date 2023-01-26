from dynamicforms_legacy import serializers, viewsets
from dynamicforms_legacy.action import Actions
from ..models import PageLoad


class PageLoadSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Dynamic page loader list',
        'new': 'New object',
        'edit': 'Editing object',
    }
    actions = Actions(add_default_crud=True, add_default_filter=True)
    show_filter = True

    class Meta:
        model = PageLoad
        exclude = ()


class PageLoadViewSet(viewsets.ModelViewSet):
    template_context = dict(url_reverse='page-load')
    pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)  # enables pagination

    queryset = PageLoad.objects.all()
    serializer_class = PageLoadSerializer
