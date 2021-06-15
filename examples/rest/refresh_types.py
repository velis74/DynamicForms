from django.utils.translation import ugettext_lazy as _

from dynamicforms import fields, serializers
from dynamicforms.action import Actions, TableAction, TablePosition
from dynamicforms.viewsets import ModelViewSet
from ..models import RefreshType


class RefreshTypesSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse='refresh-types')
    form_titles = {
        'table': 'Refresh type list',
        'new': 'New refresh type object',
        'edit': 'Editing refresh type object',
    }
    actions = Actions(
        # Add actions
        # refresh record
        TableAction(TablePosition.HEADER, label=_('+ Add (refresh record)'), title=_('Add new record'), name='add_rr',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'record', __TABLEID__);"),
        # refresh table
        TableAction(TablePosition.HEADER, label=_('+ Add (refresh table)'), title=_('Add new record'), name='add_rt',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'table', __TABLEID__);"),
        # no refresh
        TableAction(TablePosition.HEADER, label=_('+ Add (no refresh)'), title=_('Add new record'), name='add_nr',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'no refresh', __TABLEID__);"),
        # page reload
        TableAction(TablePosition.HEADER, label=_('+ Add (page reload)'), title=_('Add new record'), name='add_pr',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'page', __TABLEID__);"),
        # redirect
        TableAction(TablePosition.HEADER, label=_('+ Add (redirect)'), title=_('Add new record'), name='add_r',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'redirect:{% url 'validated-list' format='html' %}', __TABLEID__);"),
        # custom function
        TableAction(TablePosition.HEADER, label=_('+ Add (custom function)'), title=_('Add new record'), name='add_cf',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'testRefreshType', __TABLEID__);"),

        # Edit actions
        TableAction(TablePosition.ROW_CLICK, label=_('Edit'), title=_('Edit record'), name='edit_r',
                    action_js="dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' format='html'"
                              " %}'.replace('__ROWID__', $(event.target.parentElement).closest('tr[class=\"df-table-row\"]').attr('data-id'))"
                              ", 'record', __TABLEID__);"),

        # Delete actions
        # refresh record
        TableAction(TablePosition.ROW_END, label=_('Delete (refresh record)'), title=_('Delete record'), name='del_rr',
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'record', __TABLEID__);"),
        # refresh table
        TableAction(TablePosition.ROW_END, label=_('Delete (refresh table)'), title=_('Delete record'), name='del_rt',
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'table', __TABLEID__);"),
        # no refresh
        TableAction(TablePosition.ROW_END, label=_('Delete (no refresh)'), title=_('Delete record'), name='del_nr',
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'no refresh', __TABLEID__);"),
        # The following action is duplicated unnecessarily just to later eliminate it in suppress_action
        TableAction(TablePosition.ROW_END, name='del 1', label=_('Delete (no refresh)'), title=_('Delete record'),
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'no refresh', __TABLEID__);"),
        # page reload
        TableAction(TablePosition.ROW_END, label=_('Delete (page reload)'), title=_('Delete record'), name='del_pr',
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'page', __TABLEID__);"),
        # redirect
        TableAction(TablePosition.ROW_END, label=_('Delete (redirect)'), title=_('Delete record'), name='del_r',
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'redirect:{% url 'validated-list' format='html' %}', __TABLEID__);"),
        # custom function
        TableAction(TablePosition.ROW_END, label=_('Delete (custom function)'), title=_('Delete record'), name='del_cf',
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'testRefreshType', __TABLEID__);"),
    )

    rich_text_field = fields.RTFField(required=False, allow_blank=True)

    def suppress_action(self, action, request, viewset):
        if action.name == 'del 1':
            return True
        return super().suppress_action(action, request, viewset)

    class Meta:
        model = RefreshType
        exclude = ()


class RefreshTypesViewSet(ModelViewSet):
    queryset = RefreshType.objects.all()
    serializer_class = RefreshTypesSerializer
