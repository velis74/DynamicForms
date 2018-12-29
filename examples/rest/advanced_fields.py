from django.utils import timezone
from dynamicforms import serializers
from dynamicforms.viewsets import ModelViewSet
from ..models import AdvancedFields, Relation


class AdvancedFieldsSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Advanced fields list',
        'new': 'New advanced fields object',
        'edit': 'Editing advanced fields object',
    }

    regex_pattern = '(?<=abc)def'
    regex_field = serializers.RegexField(
        regex_pattern,
        error_messages={'invalid': 'This value does not match the required pattern {regex_pattern}.'.format(**locals())})

    choice_field = serializers.ChoiceField(choices=(
        (0, 'Choice 1'),
        (1, 'Choice 2'),
        (2, 'Choice 3'),
        (3, 'Choice 4'),
    ))

    hidden_field = serializers.HiddenField(default=timezone.now)
    readonly_field = serializers.ReadOnlyField()
    filepath_field = serializers.FilePathField(path='examples')

    # TODO: MultipleChoiceField
    # Problem: Not saved properly to the database. Saved as 'set()' string. Why?
    # multiplechoice_field = serializers.MultipleChoiceField(choices=(
    #     (0, 'Choice 1'),
    #     (1, 'Choice 2'),
    #     (2, 'Choice 3'),
    #     (3, 'Choice 4'),
    # ))

    # TODO: FileField, ImageField
    # file_field = serializers.FileField(required=False, use_url=True)
    # image_field = serializers.ImageField(required=False, use_url=True)

    # Error: The submitted data was not a file. Check the encoding type on the form.

    # Hints:
    # base_form.html: ectype="multipart/form-data" set on form
    # settings.py: FormParser & MultiPartParser set as DEFAULT_PARSER_CLASSES
    # urls.py: media folder added to urlpatterns (+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    # dynamicforms.js: contentType='multipart/form-data' in submitForm()
    # see how data is processed in ajax-form.js in DRF in case contentType='multipart/form-data' is used

    """ListField and DictField not supported in HTML forms in DRF"""
    # list_field = serializers.ListField()
    # dict_field = serializers.DictField()

    """JSONField available only for PostgreSQL"""
    # json_field = serilaizers.JSONField()

    """
    SerializerMethodField
    This is a read-only field. It gets its value by calling a method on the serializer class it is attached to.
    It can be used to add any sort of data to the serialized representation of your object.
    """
    # serializer_method_field = serializers.SerializerMethodField()

    """
    ModelField
    A generic field that can be tied to any arbitrary model field.
    The ModelField class delegates the task of serialization/deserialization to its associated model field.
    This field can be used to create serializer fields for custom model fields, without having to create a new custom
    serializer field.
    """
    # model_field = serializers.ModelField()

    # Relations
    string_related_field = serializers.StringRelatedField(source='primary_key_related_field')
    primary_key_related_field = serializers.PrimaryKeyRelatedField(queryset=Relation.objects.all())
    slug_related_field = serializers.SlugRelatedField(slug_field='name', queryset=Relation.objects.all())
    # hyperlinked_related_field = serializers.HyperlinkedRelatedField(view_name='relation-detail', read_only=True)
    # hyperlinked_identity_field = serializers.HyperlinkedIdentityField(view_name='relation-detail', read_only=True)

    class Meta:
        model = AdvancedFields
        exclude = ('multiplechoice_field', 'file_field', 'image_field', 'hyperlinked_related_field',
                   'hyperlinked_identity_field')

    def create(self, validated_data):
            return AdvancedFields.objects.create(**validated_data)


class AdvancedFieldsViewset(ModelViewSet):
    template_context = dict(url_reverse='advanced-fields')

    queryset = AdvancedFields.objects.all()
    serializer_class = AdvancedFieldsSerializer
