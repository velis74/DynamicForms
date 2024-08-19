from dynamicforms import serializers, viewsets
from dynamicforms.action import Actions

from ..models import PageLoad


class PageLoadSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse="page-load")
    form_titles = {
        "table": "Dynamic page loader list",
        "new": "New object",
        "edit": "Editing object",
    }

    actions = Actions(add_default_crud=True, add_default_filter=True)

    def get_row_css_style(self, obj):
        return "color: darkred"

    class Meta:
        model = PageLoad
        exclude = ()


class PageLoadViewSet(viewsets.ModelViewSet):
    template_context = dict(url_reverse="page-load")
    pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)  # enables pagination
    ordering_parameter = "sorting"
    ordering_style = "examples.pageLoadOrdering"

    queryset = PageLoad.objects.all()
    serializer_class = PageLoadSerializer
