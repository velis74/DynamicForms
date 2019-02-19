from django.db import models

from rest_framework import serializers

from dynamicforms.action import ActionControls
from dynamicforms.buttons import FormButtons, Button
from dynamicforms.settings import DYNAMICFORMS
from . import fields
from .mixins import UUIDMixIn, ActionMixin, RenderToTableMixin


class DynamicFormsSerializer(UUIDMixIn, ActionMixin, RenderToTableMixin):

    template_name = DYNAMICFORMS.form_base_template  #: template filename for single record view (HTMLFormRenderer)
    controls = ActionControls(add_default_crud=True)
    form_titles = {
        'table': '',
        'new': '',
        'edit': '',
    }
    form_buttons = FormButtons(add_default_cancel=True, add_default_save=True)

    show_filter = False  # When true, filter row is shown for list view
    serializer_type = None  # Current types: None, 'filter'

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
        if not getattr(type(self), '_filter_data', None):
            _filter_data = type(self)(instance=type(self).Meta.model())
            _filter_data.serializer_type = 'filter'
            for name, field in _filter_data.fields.fields.items():
                # if isinstance(field, fields.ChoiceField):
                #     field.allow_blank = True
                # elif isinstance(field, fields.IntegerField):
                # TODO: this doesn't work yet: the IntegerField will still have its valueset to whatever the default was
                field.allow_blank = True
                field.allow_null = True
                field.default = None
                _filter_data.data[name] = None

            type(self)._filter_data = _filter_data
        return type(self)._filter_data

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
    def renderable_actions(self):
        """
        Returns those actions that are not suppressed
        :return: List[Action]
        """
        request = self.context.get('request', None)
        viewset = self.context.get('view', None)
        return [action for action in self.controls.actions if not self.suppress_action(action, request, viewset)]


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


# noinspection PyAbstractClass
class Serializer(DynamicFormsSerializer, serializers.Serializer):
    pass
