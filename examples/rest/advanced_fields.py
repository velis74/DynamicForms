from django.utils import timezone

from dynamicforms import fields, serializers
from dynamicforms.mixins.choice import AllowTagsMixin
from dynamicforms.settings import COMPONENT_DEF_RENDERER_FORMAT
from dynamicforms.viewsets import ModelViewSet
from ..models import AdvancedFields, Relation, RelatedItem


class TaggableManyRelatedField(fields.ManyRelatedField):

    def __init__(self, *args, **kwargs):
        # kwargs["render_params"].setdefault("allow_tags", True)
        super().__init__(*args, **kwargs)
        self.render_params["allow_tags"] = True
        a = 9

    def to_internal_value(self, data):
        # try:
        return super().to_internal_value(data)
        # except Exception as e:
        #     a = 9

    # def to_representation(self, value, row_data=None):
    #     try:
    #         return super().to_representation(value, row_data)
    #     except Exception as e:
    #         a = 9

    def get_value(self, dictionary):
        try:
            return super().get_value(dictionary)
        except Exception as e:
            a = 9

    def get_choices(self, cutoff=None):
        try:
            return super().get_choices(cutoff)
        except Exception as e:
            a = 88




class RelatedItemSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse="related-items")

    class Meta:
        model = RelatedItem
        exclude = ()


class RelatedItemViewSet(ModelViewSet):
    queryset = RelatedItemSerializer.Meta.model.objects.all()

    serializer_class = RelatedItemSerializer


class AdvancedFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, is_filter: bool = False, **kwds):
        super().__init__(*args, is_filter=is_filter, **kwds)
        if self.context.get("format") == COMPONENT_DEF_RENDERER_FORMAT:
            # todo: THIS RELATIONSHIP IS NOT SUPPORTED IN VIEWMODE
            self.fields.pop("string_related_field", None)

    template_context = dict(url_reverse="advanced-fields")
    form_titles = {
        "table": "Advanced fields list",
        "new": "New advanced fields object",
        "edit": "Editing advanced fields object",
    }

    regex_pattern = "(?<=abc)def"
    single_choice_field = fields.ChoiceField(choices=(("0", "Choice 1"),), single_choice_hide=True, allow_null=True)
    hidden_field = fields.DateTimeField(default=timezone.now, display=fields.DisplayMode.HIDDEN)
    readonly_field = fields.BooleanField(read_only=True)
    # filepath_field = fields.FilePathField(path="examples")
    string_related_field = fields.StringRelatedField(source="primary_key_related_field")
    primary_key_related_field = fields.PrimaryKeyRelatedField(
        queryset=Relation.objects.all(), url_reverse="relation-list", value_field="id", text_field="name"
    )

    tags = TaggableManyRelatedField(
        child_relation=fields.PrimaryKeyRelatedField(
            queryset=RelatedItemSerializer.Meta.model.objects.all()
        ),
        url_reverse="related-items-list",
        placeholder="Assign items",
        value_field="id",
        text_field="name",
        required=False,
    )

    class Meta:
        model = AdvancedFields
        exclude = ("multiplechoice_field", "image_field", "hyperlinked_related_field", "regex_field", "filepath_field",
                   "hyperlinked_identity_field", "file_field", "file_field_two", "choice_field", "slug_related_field")

    def create(self, validated_data):
        return AdvancedFields.objects.create(**validated_data)


class AdvancedFieldsViewset(ModelViewSet):
    pagination_class = ModelViewSet.generate_paged_loader(30)

    queryset = AdvancedFields.objects.all()
    serializer_class = AdvancedFieldsSerializer

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
