from django.utils.translation import gettext_lazy as _

from dynamicforms import fields, serializers
from dynamicforms.action import Actions, TableAction, TablePosition
from dynamicforms.template_render.layout import Layout
from dynamicforms.viewsets import ModelViewSet
from ..models import BasicFields


class BasicFieldsSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse='basic-fields')
    form_titles = {
        'table': 'Basic fields list',
        'new': 'New basic fields object',
        'edit': 'Editing basic fields object',
    }
    form_template = 'examples/form_cols.html'
    component_name = 'DFFormLayout'

    actions = Actions(
        TableAction(TablePosition.HEADER, _('Modal dialog'), title=_('Dialog test'), name='modal_dialog',
                    action_js="examples.testModalDialog();"),
        TableAction(TablePosition.FIELD_END, label='field_end', title='field_end', name='field_end',
                    icon='search-outline', field_name='char_field',
                    action=dict(func_name='examples.showAlertDialog', params=dict(page='Basic fields', field='char')),
                    action_js=''),
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
    datetime_field = fields.DateTimeField()
    date_field = fields.DateField()
    time_field = fields.TimeField()
    duration_field = fields.DurationField()
    password_field = fields.CharField(password_field=True)

    class Meta:
        model = BasicFields
        exclude = ()
        layout = Layout(columns=3, size='large')


class BasicFieldsViewset(ModelViewSet):
    pagination_class = ModelViewSet.generate_paged_loader(30)

    queryset = BasicFields.objects.all()
    serializer_class = BasicFieldsSerializer
