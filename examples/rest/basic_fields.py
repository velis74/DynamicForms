from dynamicforms import serializers
from dynamicforms.viewsets import ModelViewSet
from ..models import BasicFields


class BasicFieldsSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Basic fields list',
        'new': 'New basic fields object',
        'edit': 'Editing basic fields object',
    }

    boolean_field = serializers.BooleanField()
    nullboolean_field = serializers.NullBooleanField()
    char_field = serializers.CharField()
    email_field = serializers.EmailField()
    slug_field = serializers.SlugField()
    url_field = serializers.URLField()
    uuid_field = serializers.UUIDField()
    ipaddress_field = serializers.IPAddressField()
    integer_field = serializers.IntegerField()
    float_field = serializers.IntegerField()
    decimal_field = serializers.DecimalField(max_digits=5, decimal_places=2)
    datetime_field = serializers.DateTimeField()
    date_field = serializers.DateField()
    time_field = serializers.TimeField()
    duration_field = serializers.DurationField()

    class Meta:
        model = BasicFields
        exclude = ()


class BasicFieldsViewset(ModelViewSet):
    template_context = dict(url_reverse='basic-fields')

    queryset = BasicFields.objects.all()
    serializer_class = BasicFieldsSerializer
