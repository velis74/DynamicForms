from django.utils.translation import gettext_lazy as _

from dynamicforms import fields, serializers
from dynamicforms.action import Actions, TableAction, TablePosition
from dynamicforms.viewsets import ModelViewSet
from ..models import BasicFields


class BasicFieldsSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Basic fields list',
        'new': 'New basic fields object',
        'edit': 'Editing basic fields object',
    }
    form_template = 'examples/form_cols.html'

    actions = Actions(
        TableAction(TablePosition.HEADER, _('Modal dialog'), title=_('Dialog test'), name='modal_dialog',
                    action_js="examples.testModalDialog();"),
        add_default_crud=True,
        add_form_buttons=True
    )

    boolean_field = fields.BooleanField()
    nullboolean_field = fields.NullBooleanField()
    char_field = fields.CharField()
    email_field = fields.EmailField()
    slug_field = fields.SlugField()
    url_field = fields.URLField()
    uuid_field = fields.UUIDField()
    ipaddress_field = fields.IPAddressField()
    integer_field = fields.IntegerField()
    nullint_field = fields.IntegerField(allow_null=True)
    float_field = fields.FloatField()
    decimal_field = fields.DecimalField(max_digits=5, decimal_places=2)
    datetime_field = fields.DateTimeField(required=False)
    date_field = fields.DateField()
    time_field = fields.TimeField()
    duration_field = fields.DurationField()
    password_field = fields.CharField(password_field=True)

    class Meta:
        model = BasicFields
        exclude = ()


class BasicFieldsViewset(ModelViewSet):
    template_context = dict(url_reverse='basic-fields')
    pagination_class = ModelViewSet.generate_paged_loader(30)

    queryset = BasicFields.objects.all()
    serializer_class = BasicFieldsSerializer
