import time

from dynamicforms import serializers, viewsets
from dynamicforms.action import Actions
from ..models import PageLoad


class PageLoadSerializer(serializers.ModelSerializer):

    def __init__(self, *args, is_filter: bool = False, **kwds):
        super().__init__(*args, is_filter=is_filter, **kwds)
        print('page load init', time.time(), self.is_filter)

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
