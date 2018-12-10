from dynamicforms import serializers, viewsets
from dynamicforms.action import ActionControls
from ..models import Filter


class FilterSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Dynamic filter list',
        'new': 'New object',
        'edit': 'Editing object',
    }
    controls = ActionControls(add_default_crud=True, add_default_filter=True)
    show_filter = True

    class Meta:
        model = Filter
        exclude = ()


class FilterViewSet(viewsets.ModelViewSet):
    template_context = dict(url_reverse='filter')
    pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)  # enables pagination

    queryset = Filter.objects.all()
    serializer_class = FilterSerializer
