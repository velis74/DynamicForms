from typing import Any

from django.db import models
from rest_framework import serializers

from dynamicforms.action import Actions
from dynamicforms.settings import DYNAMICFORMS
from . import fields
from .mixins import ActionMixin, RenderMixin
from .struct import StructDefault


class DynamicFormsSerializer(RenderMixin, ActionMixin):
    template_name = DYNAMICFORMS.form_base_template  #: template filename for single record view (HTMLFormRenderer)
    actions = Actions(add_default_crud=True, add_form_buttons=True)
    form_titles = {
        'table': '',
        'new': '',
        'edit': '',
    }

    show_filter = False  # When true, filter row is shown for list view

    def __init__(self, *args, is_filter: bool = False, **kwds):
        self.is_filter = is_filter
        if self.is_filter:
            try:
                instance = self.Meta.model()
                for fld in instance._meta.fields:
                    setattr(instance, fld.name, None)
            except:
                instance = StructDefault(_default_=None)
            kwds.setdefault('instance', instance)
        super().__init__(*args, **kwds)
        try:
            # hide the primary key field (DRF only marks it as R/O)
            field_name = self.Meta.model._meta.pk.name
            if field_name not in self._declared_fields:
                pk_field = self.fields[field_name]
                pk_field.display_form = fields.DisplayMode.HIDDEN
                pk_field.display_table = fields.DisplayMode.FULL
        except:
            pass
        if self.is_filter:
            for field in self.fields.values():
                field.default = None
                field.allow_blank = True
                field.allow_null = True
                field.read_only = False
                field.display_form = field.display_table  # filter's form is same as non-filter's table

    @property
    def has_non_field_errors(self):
        """
        Reports whether validation turned up any form-wide validation errors. Used in templates to render the form-wide
        error message

        :return: True | False depending on whether form validation failed
        """
        if hasattr(self, '_errors'):
            return 'non_field_errors' in self.errors
        return False

    @property
    def page_title(self):
        """
        Returns page title from form_titles based on the rendered data
        :return string: page title
        """
        if self.render_type == 'table':
            return self.form_titles.get('table', '')
        elif self.data.get('id', None):
            return self.form_titles.get('edit', '')
        else:
            return self.form_titles.get('new', '')

    # noinspection PyProtectedMember
    @property
    def filter_data(self):
        """
        Returns serializer for filter row in table
        :return:  Serializer
        """
        if getattr(self, '_filter_ser', None) is None:
            # noinspection PyAttributeOutsideInit
            self._filter_ser = type(self)(is_filter=True)
        return self._filter_ser  # Just create the same serializer in filter mode (None values, allow_nulls)

    # noinspection PyUnusedLocal
    def suppress_action(self, action, request, viewset):
        """
        Determines whether rendering an action into the DOM should be suppressed. Use when some users don't have access
        to some of the functionality, e.g. when CRUD functionality is only enabled for administrative users
        :param action: action to be checked
        :param request: request that triggered the render (may be None)
        :param viewset: viewset that provided the serialized data (may be None)
        :return: boolean whether action should render (False) or not (True)
        """
        return False

    @property
    def renderable_actions(self: 'serializers.Serializer'):
        """
        Returns those actions that are not suppressed
        :return: List[Action]
        """
        request = self.context.get('request', None)
        viewset = self.context.get('view', None)
        return [action for action in self.controls.actions if not self.suppress_action(action, request, viewset)]

    # noinspection PyUnresolvedReferences
    def get_initial(self) -> Any:
        if getattr(self, '_errors', None):
            # This basically reproduces BaseSerializer.data property except that it disregards the _errors member
            if self.instance:
                res = self.to_representation(self.instance)
            # elif hasattr(self, '_validated_data'):
            #     res = self.to_representation(self.validated_data)
            else:
                res = {}
            res.update(super().get_initial())

            return res

        return super().get_initial()


class ModelSerializer(DynamicFormsSerializer, serializers.ModelSerializer):
    """
    DynamicForms' ModelSerializer overrides the following behaviour over DRF's implementation:

    * Uses own field types for construction
    * Adds form UUID (rendered in html too)
    * Adds processing for form-wide errors

    DRF's docstring copied verbatim:

    A `ModelSerializer` is just a regular `Serializer`, except that:

    * A set of default fields are automatically populated.
    * A set of default validators are automatically populated.
    * Default `.create()` and `.update()` implementations are provided.

    The process of automatically determining a set of serializer fields
    based on the model fields is reasonably complex, but you almost certainly
    don't need to dig into the implementation.

    If the `ModelSerializer` class *doesn't* generate the set of fields that
    you need you should either declare the extra/differing fields explicitly on
    the serializer class, or simply use a `Serializer` class.
    """

    serializer_field_mapping = {
        models.AutoField: fields.IntegerField,
        models.BigIntegerField: fields.IntegerField,
        models.BooleanField: fields.BooleanField,
        models.CharField: fields.CharField,
        models.CommaSeparatedIntegerField: fields.CharField,
        models.DateField: fields.DateField,
        models.DateTimeField: fields.DateTimeField,
        models.DecimalField: fields.DecimalField,
        models.EmailField: fields.EmailField,
        models.Field: fields.ModelField,
        models.FileField: fields.FileField,
        models.FloatField: fields.FloatField,
        models.ImageField: fields.ImageField,
        models.IntegerField: fields.IntegerField,
        models.NullBooleanField: fields.NullBooleanField,
        models.PositiveIntegerField: fields.IntegerField,
        models.PositiveSmallIntegerField: fields.IntegerField,
        models.SlugField: fields.SlugField,
        models.SmallIntegerField: fields.IntegerField,
        models.TextField: fields.CharField,
        models.TimeField: fields.TimeField,
        models.URLField: fields.URLField,
        models.GenericIPAddressField: fields.IPAddressField,
        models.FilePathField: fields.FilePathField,
    }
    if models.DurationField is not None:
        serializer_field_mapping[models.DurationField] = fields.DurationField

    serializer_related_field = fields.PrimaryKeyRelatedField
    serializer_related_to_field = fields.SlugRelatedField
    serializer_url_field = fields.HyperlinkedIdentityField
    serializer_choice_field = fields.ChoiceField


class Serializer(DynamicFormsSerializer, serializers.Serializer):

    def update(self, instance, validated_data):
        # Implemented just so IDE doesn't complain. Normally this will be handled in SingleRecordViewSet
        pass

    def create(self, validated_data):
        # Implemented just so IDE doesn't complain. Normally this will be handled in SingleRecordViewSet
        pass
