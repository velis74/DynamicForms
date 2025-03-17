from django.utils import timezone

from dynamicforms import fields, serializers
from dynamicforms.template_render.layout import Layout
from dynamicforms.viewsets import ModelViewSet

from ..models import AdvancedFields, Relation


class AdvancedFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, is_filter: bool = False, **kwds):
        super().__init__(*args, is_filter=is_filter, **kwds)
        if self.context.get("format") == "componentdef":
            # todo: THIS RELATIONSHIP IS NOT SUPPORTED IN VIEWMODE
            self.fields.pop("string_related_field", None)

    template_context = dict(url_reverse="advanced-fields")
    form_titles = {
        "table": "Advanced fields list",
        "new": "New advanced fields object",
        "edit": "Editing advanced fields object",
    }

    regex_pattern = "(?<=abc)def"
    regex_field = fields.RegexField(
        regex_pattern,
        error_messages={
            "invalid": "This value does not match the required pattern {regex_pattern}.".format(**locals())
        },
        help_text="Regex pattern is (?<=abc)def",
        placeholder="Enter value that complies to regex pattern",
    )

    choice_field = fields.ChoiceField(
        choices=(
            ("0", "Choice 1"),
            ("1", "Choice 2"),
            ("2", "Choice 3"),
            ("3", "Choice 4"),
        )
    )

    single_choice_field = fields.ChoiceField(choices=(("0", "Choice 1"),), single_choice_hide=True, allow_null=True)

    hidden_field = fields.DateTimeField(default=timezone.now, display=fields.DisplayMode.HIDDEN)
    readonly_field = fields.BooleanField(read_only=True)
    filepath_field = fields.FilePathField(path="examples")

    multiplechoice_field = fields.MultipleChoiceField(
        choices=(
            (0, "Choice 1"),
            (1, "Choice 2"),
            (2, "Choice 3"),
            (3, "Choice 4"),
        )
    )

    # TODO: FileField, ImageField
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
    string_related_field = fields.StringRelatedField(source="primary_key_related_field")
    primary_key_related_field = fields.PrimaryKeyRelatedField(
        queryset=Relation.objects.all(), url_reverse="relation-list", value_field="id", text_field="name"
    )
    slug_related_field = fields.SlugRelatedField(slug_field="name", queryset=Relation.objects.all())
    file_field = fields.FileField(
        max_length=None, allow_empty_file=False, use_url=False, allow_null=True, required=False
    )
    file_field_two = fields.FileField(allow_empty_file=False, use_url=False, allow_null=True, required=False)

    # hyperlinked_identity_field = serializers.HyperlinkedIdentityField(view_name='relation-detail', read_only=True)

    class Meta:
        model = AdvancedFields
        layout = Layout(size="md")
        exclude = ("image_field", "hyperlinked_identity_field")


class AdvancedFieldsViewset(ModelViewSet):
    pagination_class = ModelViewSet.generate_paged_loader(30)

    queryset = AdvancedFields.objects.all()
    serializer_class = AdvancedFieldsSerializer

    def update(self, request, *args, **kwargs):
        # DynamicForms js client uses only PUT which makes fields checking for all fields. If you dont want to update
        # all fields e.g. upload new file, we should use PATCH method, but current js client does not support this.
        # To enable update of record without re-uploading new file,
        # we enable partial update with line below -> kwargs['partial'] = True
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
