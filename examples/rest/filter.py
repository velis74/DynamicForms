from dynamicforms import serializers, viewsets
from dynamicforms.action import Actions
from dynamicforms.fields import DateTimeField, RTFField
from examples.rest.fields.name_field import NameTestField

from ..models import Filter


class FilterSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse="filter")
    form_titles = {
        "table": "Dynamic filter list",
        "new": "New object",
        "edit": "Editing object",
    }
    actions = Actions(add_default_filter=True, add_default_crud=True, add_form_buttons=True)

    name = NameTestField(
        label="Name field",
        max_length=list(filter(lambda f: f.name == "name", Filter._meta.fields))[0].max_length,
        allow_null=list(filter(lambda f: f.name == "name", Filter._meta.fields))[0].null,
        source="*",
    )
    rtf_field = RTFField(required=False, allow_null=True)
    datetime_field = DateTimeField(
        label="Datetime field",
        render_params=dict(
            table_format="dd.MM.yyyy HH:mm",
            form_format="dd.MM.yyyy HH:mm",
        ),
    )

    class Meta:
        model = Filter
        exclude = ()


class FilterViewSet(viewsets.ModelViewSet):
    pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)  # enables pagination

    queryset = Filter.objects.all()
    serializer_class = FilterSerializer
