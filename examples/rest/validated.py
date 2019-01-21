from django.utils.translation import ugettext_lazy as _
from dynamicforms import serializers
from dynamicforms.action import Action, ActionControls
from dynamicforms.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from ..models import Validated


class ValidatedSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Validated list',
        'new': 'New validated object',
        'edit': 'Editing validated object',
    }
    controls = ActionControls([
        Action(label=_('+ Add (refresh record)'), title=_('Add new record'), icon='', position='header',
               action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}', refreshType='record');"),
        Action(label=_('+ Add (refresh table)'), title=_('Add new record'), icon='', position='header',
               action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}', refreshType='table');"),
        Action(label=_('+ Add (no refresh)'), title=_('Add new record'), icon='', position='header',
               action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}', refreshType='no refresh');"),
        Action(label=_('Edit'), title=_('Edit record'), icon='', position='rowclick',
               action="dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' format='html'"
                      " %}'.replace('__ROWID__', $(event.target.parentElement).attr('data-id')), refreshType='record');"),
        Action(label=_('Delete (refresh record)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
               + "deleteThisRow={{row.id}}, refreshType='record');"),
        Action(label=_('Delete (refresh table)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
               + "deleteThisRow={{row.id}}, refreshType='table');"),
        Action(label=_('Delete (no refresh)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
               + "deleteThisRow={{row.id}}, refreshType='no refresh');"),
        # The following action is duplicated unnecessarily just to later eliminate it in suppress_action
        Action(name='del 1', label=_('Delete (no refresh)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                      + "deleteThisRow={{row.id}}, refreshType='no refresh');")
    ])

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
    template_context = dict(url_reverse='validated')

    queryset = Validated.objects.all()
    serializer_class = ValidatedSerializer
