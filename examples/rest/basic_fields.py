from dynamicforms import fields, serializers
from dynamicforms.viewsets import ModelViewSet
from ..models import BasicFields


class BasicFieldsSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Basic fields list',
        'new': 'New basic fields object',
        'edit': 'Editing basic fields object',
    }
    form_template = 'examples/form_cols.html'

    boolean_field = fields.BooleanField()
    nullboolean_field = fields.NullBooleanField()
    char_field = fields.CharField()
    email_field = fields.EmailField()
    slug_field = fields.SlugField()
    url_field = fields.URLField()
    uuid_field = fields.UUIDField()
    ipaddress_field = fields.IPAddressField()
    integer_field = fields.IntegerField()
    float_field = fields.IntegerField()
    decimal_field = fields.DecimalField(max_digits=5, decimal_places=2)
    datetime_field = fields.DateTimeField()
    date_field = fields.DateField()
    time_field = fields.TimeField()
    duration_field = fields.DurationField()

    class Meta:
        model = BasicFields
        exclude = ()


class BasicFieldsViewset(ModelViewSet):
    template_context = dict(url_reverse='basic-fields')

    queryset = BasicFields.objects.all()
    serializer_class = BasicFieldsSerializer
