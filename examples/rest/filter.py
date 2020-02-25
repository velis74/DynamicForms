from dynamicforms import serializers, viewsets
from dynamicforms.action import Actions
from examples.rest.fields.name_field import NameTestField
from ..models import Filter


class FilterSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Dynamic filter list',
        'new': 'New object',
        'edit': 'Editing object',
    }
    actions = Actions(add_default_crud=True, add_default_filter=True)
    show_filter = True

    name = NameTestField(
        label='Name field',
        max_length=list(filter(lambda f: f.name == 'name', Filter._meta.fields))[0].max_length,
        allow_null=list(filter(lambda f: f.name == 'name', Filter._meta.fields))[0].null,
        source='*',
    )

    class Meta:
        model = Filter
        exclude = ()


class FilterViewSet(viewsets.ModelViewSet):
    template_context = dict(url_reverse='filter')
    pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)  # enables pagination

    queryset = Filter.objects.all()
    serializer_class = FilterSerializer
