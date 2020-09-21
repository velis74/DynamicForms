from django.utils.translation import ugettext_lazy as _

from dynamicforms import serializers, viewsets
from dynamicforms.action import Actions, TableAction, TablePosition
from examples.rest.fields.name_field import NameTestField
from ..models import Filter


class FilterSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse='filter')
    form_titles = {
        'table': 'Dynamic filter list',
        'new': 'New object',
        'edit': 'Editing object',
    }
    actions = Actions(
        TableAction(TablePosition.FILTER_ROW_END, _('+ Add'), title=_('Add new record'), name='add',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'record', __TABLEID__);"),
        TableAction(TablePosition.ROW_CLICK, _('Edit'), title=_('Edit record'), name='edit',
                    action_js="dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' "
                              "format='html' %}'.replace('__ROWID__', $(event.target.parentElement).closest('tr[class=\"df-table-row\"]').attr('data-id')), 'record', __TABLEID__);"),
        TableAction(TablePosition.ROW_END, label=_('Delete'), title=_('Delete record'), name='delete',
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              "{{row.id}}, 'record', __TABLEID__);"),
        TableAction(TablePosition.FILTER_ROW_END, label=_('Filter'), title=_('Filter'), name='filter',
                    action_js="dynamicforms.defaultFilter(event);")
    )
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
    pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)  # enables pagination

    queryset = Filter.objects.all()
    serializer_class = FilterSerializer
