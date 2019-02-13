from django.utils.translation import ugettext_lazy as _
from dynamicforms import serializers
from dynamicforms.action import Action, ActionControls
from dynamicforms.viewsets import ModelViewSet
from ..models import RefreshType


class RefreshTypesSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Refresh type list',
        'new': 'New refresh type object',
        'edit': 'Editing refresh type object',
    }
    controls = ActionControls([
        # Add actions
        # refresh record
        Action(label=_('+ Add (refresh record)'), title=_('Add new record'), icon='', position='header',
               action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                      ", 'record', __TABLEID__);"),
        # refresh table
        Action(label=_('+ Add (refresh table)'), title=_('Add new record'), icon='', position='header',
               action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                      ", 'table', __TABLEID__);"),
        # no refresh
        Action(label=_('+ Add (no refresh)'), title=_('Add new record'), icon='', position='header',
               action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                      ", 'no refresh', __TABLEID__);"),
        # page reload
        Action(label=_('+ Add (page reload)'), title=_('Add new record'), icon='', position='header',
               action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                      ", 'page', __TABLEID__);"),
        # redirect
        Action(label=_('+ Add (redirect)'), title=_('Add new record'), icon='', position='header',
               action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                      ", 'redirect:{% url 'validated-list' format='html' %}', __TABLEID__);"),
        # custom function
        Action(label=_('+ Add (custom function)'), title=_('Add new record'), icon='', position='header',
               action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                      ", 'testRefreshType', __TABLEID__);"),

        # Edit actions
        Action(label=_('Edit'), title=_('Edit record'), icon='', position='rowclick',
               action="dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' format='html'"
                      " %}'.replace('__ROWID__', $(event.target.parentElement).attr('data-id'))"
                      ", 'record', __TABLEID__);"),

        # Delete actions
        # refresh record
        Action(label=_('Delete (refresh record)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
               + "{{row.id}}, 'record', __TABLEID__);"),
        # refresh table
        Action(label=_('Delete (refresh table)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
               + "{{row.id}}, 'table', __TABLEID__);"),
        # no refresh
        Action(label=_('Delete (no refresh)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
               + "{{row.id}}, 'no refresh', __TABLEID__);"),
        # The following action is duplicated unnecessarily just to later eliminate it in suppress_action
        Action(name='del 1', label=_('Delete (no refresh)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                      + "{{row.id}}, 'no refresh', __TABLEID__);"),
        # page reload
        Action(label=_('Delete (page reload)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
               + "{{row.id}}, 'page', __TABLEID__);"),
        # redirect
        Action(label=_('Delete (redirect)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
               + "{{row.id}}, 'redirect:{% url 'validated-list' format='html' %}', __TABLEID__);"),
        # custom function
        Action(label=_('Delete (custom function)'), title=_('Delete record'), icon='', position='rowend',
               action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
               + "{{row.id}}, 'testRefreshType', __TABLEID__);"),
    ])

    def suppress_action(self, action, request, viewset):
        if action.name == 'del 1':
            return True
        return super().suppress_action(action, request, viewset)

    class Meta:
        model = RefreshType
        exclude = ()


class RefreshTypesViewSet(ModelViewSet):
    template_context = dict(url_reverse='refresh-types')

    queryset = RefreshType.objects.all()
    serializer_class = RefreshTypesSerializer
