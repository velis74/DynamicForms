from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from dynamicforms import serializers
from dynamicforms.action import Actions, TableAction, TablePosition
from dynamicforms.viewsets import ModelViewSet
from ..models import Validated


class ValidatedSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse='validated')
    form_titles = {
        'table': 'Validated list',
        'new': 'New validated object',
        'edit': 'Editing validated object',
    }
    actions = Actions(
        TableAction(TablePosition.HEADER, label=_('+ Add (refresh record)'), title=_('Add new record'), name='add',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'record', __TABLEID__);"),
        TableAction(TablePosition.HEADER, label=_('+ Add (refresh table)'), title=_('Add new record'), name='add_rt',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'table', __TABLEID__);"),
        TableAction(TablePosition.HEADER, label=_('+ Add (no refresh)'), title=_('Add new record'), name='add_nr',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'no refresh', __TABLEID__);"),
        TableAction(TablePosition.ROW_CLICK, label=_('Edit'), title=_('Edit record'), name='edit',
                    action_js="dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' format='html'"
                              " %}'.replace('__ROWID__', $(event.target.parentElement).closest('tr[class=\"df-table-"
                              "row\"]').attr('data-id')), 'record', __TABLEID__);"),
        TableAction(TablePosition.ROW_END, label=_('Delete (refresh record)'), title=_('Delete record'), name='delete',
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'record', __TABLEID__);"),
        TableAction(TablePosition.ROW_END, label=_('Delete (refresh table)'), title=_('Delete record'), name='del_rt',
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'table', __TABLEID__);"),
        TableAction(TablePosition.ROW_END, label=_('Delete (no refresh)'), title=_('Delete record'), name='del_nr',
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'no refresh', __TABLEID__);"),
        # The following action is duplicated unnecessarily just to later eliminate it in suppress_action
        TableAction(TablePosition.ROW_END, name='del 1', label=_('Delete (no refresh)'), title=_('Delete record'),
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'no refresh', __TABLEID__);")
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['amount'] != 5:
            if attrs['code'] != '123':
                raise ValidationError({'amount': 'amount can only be different than 5 if code is "123"'})

        if attrs['enabled'] is True and attrs['item_type'] == 3:
            raise ValidationError('When enabled you can only choose from first three item types')

        return attrs

    def suppress_action(self, action, request, viewset):
        if action.name == 'del 1':
            return True
        return super().suppress_action(action, request, viewset)

    class Meta:
        model = Validated
        exclude = ()


class ValidatedViewSet(ModelViewSet):
    queryset = Validated.objects.all()
    serializer_class = ValidatedSerializer
