from collections import OrderedDict
from typing import Any

from django.db import models
from rest_framework import serializers
from rest_framework.fields import SkipField

from dynamicforms.action import Actions
from dynamicforms.settings import DYNAMICFORMS
from . import fields
from .mixins import ActionMixin, DisplayMode, RenderMixin
from .struct import StructDefault


class DynamicFormsSerializer(RenderMixin, ActionMixin):
    template_context = {}  # see ViewSet.template_context
    template_name = DYNAMICFORMS.form_base_template  #: template filename for single record view (HTMLFormRenderer)
    actions = Actions(add_default_crud=True, add_form_buttons=True)
    form_titles = {
        'table': '',
        'new': '',
        'edit': '',
    }

    show_filter = False  # When true, filter row is shown for list view

    def __init__(self, *args, is_filter: bool = False, **kwds):
        self.master = None
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
                field.allow_tags = False

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
            self._filter_ser = type(self)(is_filter=True, context=getattr(self, 'context', {}))
            self._filter_ser.master = self
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
        # TODO: Ta funkcija po mojem mora odletet (self.*controls*.actions). Sam zakaj ne? Ali se sploh ne uporablja?
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

    # noinspection PyUnresolvedReferences
    @property
    def _writable_fields(self):
        """
        Overrides DRF.serializers.Serializer._writable_fields
        This one in particular should return exactly the same list as DRF's version (as of 17.4.2020, DRF version 3.11
        """
        return (
            field for field in self.fields.values()
            if not field.read_only
        )

    # noinspection PyUnresolvedReferences
    @property
    def _readable_fields(self):
        """
        Overrides DRF.serializers.Serializer._readable_fields
        This one adds additional checks on top of DRF's ones - checking if the field is renderable to table or form
        """
        return (
            field for field in self.fields.values()
            if not (field.write_only
                    or (self.is_rendering_to_list and self.display_table == DisplayMode.SUPPRESS)
                    or (not self.is_rendering_to_list and self.display_form == DisplayMode.SUPPRESS)
                    )
        )

    def to_representation(self, instance, row_data=None):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        for field in self._readable_fields:
            try:
                attribute = field.get_attribute(instance)
                ret[field.field_name] = field.to_representation(attribute, row_data)
            except SkipField:
                pass

        return ret


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

    def __init__(self, *args, is_filter: bool = False, **kwds):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'fields'):
            self._make_df_special_fields_present_in_fields(['df_prev_id', 'row_css_style'])
        super().__init__(*args, is_filter=is_filter, **kwds)
        self.manage_changed_flds()

    def _make_df_special_fields_present_in_fields(self, fields):
        for f in fields:
            if self.Meta.fields != '__all__' and f not in self.Meta.fields:
                self.Meta.fields += f,

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

    def manage_changed_flds(self):
        """
        When there is a need to only change few parameters of a field put those fields and changed parameters in
        serializers Meta class in parameter changed_flds.

        Example:

        .. code-block:: python

           changed_flds = {
               'id': dict(display=DisplayMode.HIDDEN),
               'comment': dict(label='Comm', help_text='Help text for comment field')
           }

        :return:

        """
        if hasattr(self.Meta, 'changed_flds'):
            for field, params in self.Meta.changed_flds.items():
                field_def = self.fields.get(field, None)
                if field_def:
                    for key, val in params.items():
                        setattr(field_def, key, val)

    # Dynamic forms default field that is used to contain data for positioning (id of previous record)
    df_prev_id = fields.SerializerMethodField(display=DisplayMode.HIDDEN)

    # this is a calculated field that returns css style for table row
    row_css_style = fields.SerializerMethodField(display=DisplayMode.HIDDEN)

    def fetch_prev_id(self, obj, view):
        ordering = 'id'
        try:
            ordering = view.pagination_class.ordering
        except:
            pass
        if ordering != 'id':
            query_params = self.context['request'].query_params
            query_params._mutable = True
            query_params.pop('id', '')
            queryset = view.filter_queryset(queryset=view.get_queryset(), query_params=query_params)
            records = list(queryset.order_by(ordering))
            curr_index = records.index(obj)
            prev_id = None
            if curr_index > 0:
                prev_id = records[curr_index - 1].id

            return prev_id

        return ''

    # noinspection PyMethodMayBeStatic
    def get_df_prev_id(self, obj):
        try:
            if self.context['request'].META.get('HTTP_X_DF_CALLTYPE', '') == 'refresh_record':
                view = self.context.get('view', None)
                if view:
                    return self.fetch_prev_id(obj, view)
        except:
            pass

        return ''

    # noinspection PyMethodMayBeStatic
    def get_row_css_style(self, obj):
        return ''


class Serializer(DynamicFormsSerializer, serializers.Serializer):

    def update(self, instance, validated_data):
        # Implemented just so IDE doesn't complain. Normally this will be handled in SingleRecordViewSet
        pass

    def create(self, validated_data):
        # Implemented just so IDE doesn't complain. Normally this will be handled in SingleRecordViewSet
        pass
