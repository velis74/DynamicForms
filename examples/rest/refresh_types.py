from dynamicforms import fields, serializers
from dynamicforms.action import Actions
from dynamicforms.viewsets import ModelViewSet
from ..models import RefreshType


class RefreshTypesSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse='refresh-types')
    form_titles = {
        'table': 'Refresh type list',
        'new': 'New refresh type object',
        'edit': 'Editing refresh type object',
    }
    actions = Actions(add_form_buttons=True, add_default_crud=True, add_default_filter=False)

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
