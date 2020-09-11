import django_filters.rest_framework as filters


class ListWithFields(list):

    def __init__(self, fields, lst) -> None:
        super().__init__()
        self.fields = fields
        self.extend(lst)


class FilterBackend(filters.DjangoFilterBackend):

    def get_filterset_class(self, view, queryset=None):

        ordering_excluded_fields = getattr(view, 'filterset_ordering_exclude', [])
        ordering_default = getattr(view, 'filterset_ordering_default', ['id'])

        class MyOrderingFilter(filters.OrderingFilter):
            def get_ordering(self, value):
                if not value:
                    return ListWithFields(list(self.param_map.keys()), ordering_default)
                return ListWithFields(list(self.param_map.keys()), [self.get_ordering_value(param) for param in value])

        class FilterSetApplied(filters.FilterSet):
            ordering = MyOrderingFilter(
                fields=[f.name for f in queryset.model._meta.fields if f.name not in ordering_excluded_fields]
            )

        return FilterSetApplied

    def get_ordering(self, request, queryset, view):
        filterset = self.get_filterset(request, queryset, view)
        filterset.is_valid()
        ordering_filters = {k: v for k, v in filterset.filters.items() if isinstance(v, filters.OrderingFilter)}
        for name, value in filterset.form.cleaned_data.items():
            if name in ordering_filters:
                return ordering_filters[name].get_ordering(value)
