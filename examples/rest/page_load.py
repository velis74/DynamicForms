from dynamicforms import serializers, viewsets
from ..models import PageLoad


class PageLoadSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse='page-load')
    form_titles = {
        'table': 'Dynamic page loader list',
        'new': 'New object',
        'edit': 'Editing object',
    }
    """
    actions = Actions(
        TableAction(TablePosition.FIELD_START, label='field_start', title='field_start',
                    name='field_start',
                    icon='pencil-outline', field_name='description',
                    action=dict(func_name='examples.showAlertDialog',
                                params=dict(page='Page load', field='description')),
                    action_js=''),
        TableAction(TablePosition.FIELD_END, label='field_end', title='field_end', name='field_end',
                    icon='search-outline', field_name='choice',
                    action=dict(func_name='examples.showAlertDialog',
                                params=dict(page='Page load', field='choice')),
                    action_js=''),
        add_default_crud=True, add_default_filter=True)
    """
    show_filter = True

    def get_row_css_style(self, obj):
        return 'color: darkred'

    class Meta:
        model = PageLoad
        exclude = ()


class PageLoadViewSet(viewsets.ModelViewSet):
    template_context = dict(url_reverse='page-load')
    pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)  # enables pagination

    queryset = PageLoad.objects.all()
    serializer_class = PageLoadSerializer
