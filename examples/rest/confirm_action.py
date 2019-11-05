import random

from rest_framework.permissions import SAFE_METHODS

from dynamicforms import serializers
from dynamicforms.action import Actions, TableAction, TablePosition, FormButtonTypes, FormButtonAction
from dynamicforms.viewsets import ModelViewSet
from ..models import ConfirmAction


class ConfirmActionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, is_filter: bool = False, **kwds):
        super().__init__(*args, is_filter=is_filter, **kwds)
        if self.context['request'].method in SAFE_METHODS and self.context['view'].kwargs.get('pk') == 'new':
            submit_action = list(filter(lambda a: a.name == 'submit', self.actions.actions))
            submit_confirm_action = list(filter(lambda a: a.name == 'submit-confirm', self.actions.actions))
            if submit_action:
                self.actions.actions.remove(
                    submit_action[0])
            if submit_confirm_action:
                self.actions.actions.remove(
                    submit_confirm_action[0])
        elif self.context['request'].method in SAFE_METHODS and self.context['view'].kwargs.get('pk'):
            save_action = list(filter(lambda a: a.name == 'save', self.actions.actions))
            if save_action:
                self.actions.actions.remove(
                    save_action[0])
            submit_action = list(filter(lambda a: a.name == 'submit', self.actions.actions))
            if submit_action:
                self.actions.actions.remove(
                    submit_action[0])

    form_titles = {
        'table': 'Actions list',
        'new': 'New action object',
        'edit': 'Editing action object',
    }

    actions = Actions(
        TableAction(TablePosition.ROW_END,
                    label='Delete item with confirmation',
                    title='Delete item',
                    name='delete-confirm',
                    action_js="dynamicforms.deleteRowWithConfirmation("
                              "'{% url url_reverse|add:'-detail' pk=row.id %}', "
                              "{{row.id}}, 'record', __TABLEID__);"),
        FormButtonAction(
            btn_type=FormButtonTypes.CUSTOM, label='Save', name='save', positions=['dialog'],
            button_is_primary=True,
            action_js="var $dlg = $('#dialog-{self.serializer.uuid}');"
                      "var $form = $('#{self.serializer.uuid}');"
                      "dynamicforms.submitFormWithConfirmation("
                      "'{{% url url_reverse|add:'-list' %}}', "
                      "$dlg, $form);"),
        TableAction(TablePosition.HEADER, '+ Add new action', title='Add new action', name='add',
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}',"
                              "'record', __TABLEID__);"),
        TableAction(TablePosition.ROW_CLICK, 'Edit', title='Edit action', name='edit',
                    action_js="dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' "
                              "format='html' %}'.replace('__ROWID__', $(event.target).parents('tr')."
                              "attr('data-id')), 'record', __TABLEID__);"),
        FormButtonAction(
            btn_type=FormButtonTypes.CUSTOM, label='Save changes', name='submit-confirm',
            positions=['dialog'],
            button_is_primary=True,
            action_js="var $dlg = $('#dialog-{self.serializer.uuid}');"
                      "var $form = $('#{self.serializer.uuid}');"
                      "dynamicforms.submitFormWithConfirmation("
                      "(('{{% url 'confirm-action-detail' pk='__ROWID__' %}}').replace("
                      "'__ROWID__', $form.find('input[name=\"id\"]').val())), $dlg, $form);"),
        TableAction(TablePosition.ROW_END, 'View readonly details', title='View readonly details',
                    name='view-details',
                    action_js="dynamicforms.showReadOnlyRow("
                              "'{% url 'confirm-action-view-readonly-detail' pk='__ROWID__' "
                              "format='html' %}'.replace('__ROWID__', $(event.target).parents('tr')."
                              "attr('data-id')), __TABLEID__);"),
        add_default_crud=False,
        add_default_filter=False,
    )

    def confirm_delete_text(self, request, model_instance):
        return "{} {}: {}.".format(
            'Do you really want to delete selected record?',
            'Record',
            str(model_instance)
        )

    def confirm_delete_title(self):
        return 'Delete item confirmation'

    def confirm_create_text(self):
        return 'Do you really want to create item?'

    def confirm_create_title(self):
        return 'Create new item'

    def confirm_update_text(self):
        return 'Do you really want to update item?'

    def confirm_update_title(self):
        return 'Update item'

    def is_row_editable(self, row_data: object) -> bool:
        if row_data and row_data.get('enabled'):
            return True
        return False

    class Meta:
        model = ConfirmAction
        exclude = ()


class ConfirmActionViewSet(ModelViewSet):
    template_context = dict(url_reverse='confirm-action')
    queryset = ConfirmAction.objects.all()
    serializer_class = ConfirmActionSerializer
