from dynamicforms import serializers
from dynamicforms.action import Actions, TableAction, TablePosition
from dynamicforms.viewsets import ModelViewSet
from ..models import ConfirmAction


class ConfirmActionSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = ConfirmAction
        exclude = ()


class ConfirmActionViewSet(ModelViewSet):
    template_context = dict(url_reverse='confirm-action')
    queryset = ConfirmAction.objects.all()
    serializer_class = ConfirmActionSerializer
