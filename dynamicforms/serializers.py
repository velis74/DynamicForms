from collections import OrderedDict
from typing import Any, Dict, List, Optional

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.fields.related import RelatedField
from django.utils.module_loading import import_string
from rest_framework import serializers
from rest_framework.fields import get_attribute, SkipField

from dynamicforms.action import Actions
from dynamicforms.template_render import ViewModeSerializer

from . import fields
from .mixins import ActionMixin, DisplayMode, FieldRenderMixin
from .models_fields import ColorField, EnumChoiceField
from .struct import StructDefault
from .utils import get_pk_name


class DynamicFormsSerializer(ViewModeSerializer, FieldRenderMixin, ActionMixin):
    template_context = {}  # see ViewSet.template_context
    actions = Actions(add_default_crud=True, add_form_buttons=True)
    form_titles = {
        "table": "",
        "new": "",
        "edit": "",
    }

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
            kwds.setdefault("instance", instance)
        super().__init__(*args, **kwds)
        if self.is_filter:
            for field_name, field in self.fields.items():
                field.default = None
                field.allow_blank = True
                field.allow_null = True
                field.read_only = False
                # the following ifs are actually redundant because front-end code currently doesn't even obey this
                # it always renders the columns as visible in the table, except that in filter row, it takes
                # the non-display fields for filtering instead of the resolved texts that can't be filtered
                if (field_name + "-display") in self.fields.keys():
                    # if field has a resolved display counterpart (Choice, Related), show the original field
                    pass
                elif field_name.endswith("-display"):
                    # if field is the resolved display counterpart, don't show it in filter row
                    pass
                else:
                    field.display_form = field.display_table  # filter's form is same as non-filter's table
                field.allow_tags = False
                field.password_field = False

    @property
    def has_non_field_errors(self):
        """
        Reports whether validation turned up any form-wide validation errors. Used in templates to render the form-wide
        error message

        :return: True | False depending on whether form validation failed
        """
        if hasattr(self, "_errors"):
            return "non_field_errors" in self.errors
        return False

    @property
    def page_title(self):
        """
        Returns page title from form_titles based on the rendered data
        :return string: page title
        """
        if self.render_type == "table":
            return self.form_titles.get("table", "")
        elif self.data.get("id", None):
            return self.form_titles.get("edit", "")
        else:
            return self.form_titles.get("new", "")

    # noinspection PyProtectedMember
    @property
    def filter_data(self):
        """
        Returns serializer for filter row in table
        :return:  Serializer
        """
        if self.view_mode == ViewModeSerializer.ViewMode.FORM:
            return None
        if getattr(self, "_filter_ser", None) is None:
            # noinspection PyAttributeOutsideInit
            self._filter_ser = type(self)(is_filter=True, context=getattr(self, "context", {}))
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
    def renderable_actions(self: "serializers.Serializer"):
        """
        Returns those actions that are not suppressed
        :return: List[Action]
        """
        # TODO: Ta funkcija po mojem mora odletet (self.*controls*.actions). Sam zakaj ne? Ali se sploh ne uporablja?
        request = self.context.get("request", None)
        viewset = self.context.get("view", None)
        return [action for action in self.controls.actions if not self.suppress_action(action, request, viewset)]

    # noinspection PyUnresolvedReferences
    def get_initial(self) -> Any:
        if getattr(self, "_errors", None):
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
        return (field for field in self.fields.values() if not field.read_only)

    # noinspection PyUnresolvedReferences
    @property
    def _readable_fields(self):
        """
        Overrides DRF.serializers.Serializer._readable_fields
        This one adds additional checks on top of DRF's ones - checking if the field is renderable to table or form
        """
        return (
            field
            for field in self.fields.values()
            if not (
                field.write_only
                or (self.display_table == DisplayMode.SUPPRESS and self.display_form == DisplayMode.SUPPRESS)
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
                if not isinstance(field, FieldRenderMixin):
                    ret[field.field_name] = field.to_representation(attribute)
                else:
                    try:
                        ret[field.field_name] = field.to_representation(attribute, instance)
                    except:
                        if attribute is None and not field.required:
                            # DRF makes a special check for none and then always returns None if the check is None.
                            # We still want to process custom field to_representation, even if value is None.
                            # But when field is a sub-serializer and it (it's FK reference) is none, it's OK
                            # to pass None as result of serialization of such field
                            raise SkipField()
                        else:
                            raise
            except SkipField:
                pass

        return ret

    # noinspection PyMethodMayBeStatic
    def get_row_css_style(self, obj):
        return ""


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
        if hasattr(self, "Meta") and hasattr(self.Meta, "fields"):
            self._make_df_special_fields_present_in_fields(["df_prev_id", "row_css_style", "df_control_data"])
        super().__init__(*args, is_filter=is_filter, **kwds)
        self.manage_changed_flds()
        self._decorate_fields()

    def _decorate_fields(self):
        def pop(self, name: str, default):
            super(self.__class__, self).pop(name, default)
            super(self.__class__, self).pop(name + "-display", None)

        self.fields.pop = pop.__get__(self.fields)
        # copy the labels to resolved -display fields
        for field in self.fields:
            if field.endswith("-display"):
                self.fields[field].label = self.fields[field[:-8]].label

    def _make_df_special_fields_present_in_fields(self, fields):
        for f in fields:
            if self.Meta.fields != "__all__" and f not in self.Meta.fields:
                self.Meta.fields += (f,)

    serializer_field_mapping = {
        models.AutoField: fields.IntegerField,
        models.BigIntegerField: fields.IntegerField,
        models.BooleanField: fields.BooleanField,
        models.NullBooleanField: fields.BooleanField,
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
        models.PositiveIntegerField: fields.IntegerField,
        models.PositiveSmallIntegerField: fields.IntegerField,
        models.SlugField: fields.SlugField,
        models.SmallIntegerField: fields.IntegerField,
        models.TextField: fields.CharField,
        models.TimeField: fields.TimeField,
        models.URLField: fields.URLField,
        models.GenericIPAddressField: fields.IPAddressField,
        models.FilePathField: fields.FilePathField,
        models.JSONField: fields.JSONField,
        EnumChoiceField: fields.ChoiceField,
        ColorField: fields.ColorField,
    }
    if models.DurationField is not None:
        serializer_field_mapping[models.DurationField] = fields.DurationField

    serializer_related_field = fields.PrimaryKeyRelatedField
    serializer_related_to_field = fields.SlugRelatedField
    serializer_url_field = fields.HyperlinkedIdentityField
    serializer_choice_field = fields.ChoiceField

    def get_field_names(self, declared_fields, info):
        # we're just converting DRF's tuple to list here because we need it modifiable in get_uniqueness_extra_kwargs
        return list(super().get_field_names(declared_fields, info))

    def get_extra_kwargs(self):
        res = super().get_extra_kwargs()
        # noinspection PyUnresolvedReferences
        for fld in self.Meta.model._meta.fields:
            # We're exploiting DRF design "feature" here where DRF only perceives a field as declared if it's a Field
            #  instance. AutoGeneratedField is not a Field instance and will thus be overwritten by auto generated field
            # Note how Field instances are already removed from the class here.
            #  They reappear in the get_uniqueness_extra_kwargs method below
            fld_name = fld.db_column or fld.name
            value = getattr(self, fld_name, None)
            if isinstance(value, fields.AutoGeneratedField):
                res.setdefault(fld_name, {})
                res[fld_name].update(value)
        return res

    def get_uniqueness_extra_kwargs(self, field_names: List[str], declared_fields: Dict, extra_kwargs: Dict):
        """
        Finds all ChoiceFields and RelatedFields and creates additional "-display" fields to show
        resolved display value in table
        """
        for field_name in field_names[:]:
            # existing extra as provided by get_extra_kwargs
            extra = extra_kwargs.get(field_name, dict())

            # serializer field: either what is declared as a Field instance in Serializer or AutogeneratedField
            s_field = declared_fields.get(field_name, getattr(self, field_name, None))
            if isinstance(s_field, fields.AutoGeneratedField):
                s_field = s_field.get_serializer_field(field_name, self, extra)

            # model field, if it exists
            try:
                d_field = self.Meta.model._meta.get_field(field_name)
            except FieldDoesNotExist:
                d_field = None

            if d_field and d_field.name == get_pk_name(self.Meta.model):
                # hide the primary key field (DRF only marks it as R/O)
                field_name = get_pk_name(self.Meta.model)
                if field_name not in declared_fields and "display" not in extra:
                    extra.setdefault("display_form", fields.DisplayMode.HIDDEN)
                    extra.setdefault("display_table", fields.DisplayMode.FULL)
                    extra_kwargs[field_name] = extra

            if isinstance(s_field, (fields.ChoiceMixin, fields.RelatedFieldAJAXMixin)) or (
                # if custom field properties are declared and they are either ChoiceField or RelatedField
                isinstance(d_field, RelatedField)  # DB field is a relation
                or getattr(d_field, "choices", None)  # DB field has choices
            ):
                if (s_field and getattr(s_field, "display_table", DisplayMode.SUPPRESS) == DisplayMode.SUPPRESS) or (
                    hasattr(self, "Meta") and hasattr(self.Meta, "exclude") and field_name in self.Meta.exclude
                ):
                    # if the field is set to not display in the table, don't create the resolved field
                    continue
                s_field_display_table = (s_field.display_table if s_field else None) or DisplayMode.FULL
                # original field does not display in the table
                if field_name in declared_fields:
                    # declared fields cannot also have extra_kwargs (there is a continue in the loop)
                    s_field.display_table = DisplayMode.HIDDEN
                else:
                    extra["display_table"] = DisplayMode.HIDDEN
                    extra_kwargs[field_name] = extra

                resolved_field_name = f"{field_name}-display"
                # if resolved_field_name in declared_fields or resolved_field_name in extra_kwargs:
                #     raise ValueError(f"We were going to add a table resolved field '{resolved_field_name}' but "
                #                      f"a field with this name is already declared in "
                #                      f"the serializer {self.__class__.__name__")
                field_names.insert(field_names.index(field_name) + 1, resolved_field_name)
                declared_fields[resolved_field_name] = fields.SerializerMethodField(
                    source="*",
                    display_form=DisplayMode.HIDDEN,
                    display_table=s_field_display_table,
                    render_params=getattr(s_field, "render_params", None) if s_field else None,
                )

                def get_resolve_method(fld_nm, res_fld):
                    def resolve_choice_field(self, value):
                        from dynamicforms.fields import ManyRelatedField

                        if (
                            isinstance(self.fields[fld_nm], ManyRelatedField)
                            and value
                            and not getattr(value, "pk", None)
                        ):
                            return None

                        source_attr = self.fields[fld_nm].source_attrs
                        row_data = value
                        try:
                            value = get_attribute(value, source_attr)
                        except:
                            value = None

                        return self.fields[fld_nm].render_to_table(
                            # getattr has a default == None because the object might be a new init and
                            #   will not have relations
                            value,
                            row_data,
                        )

                    return resolve_choice_field

                setattr(
                    self,
                    f"get_{resolved_field_name}",
                    get_resolve_method(field_name, resolved_field_name).__get__(self),
                )

                if hasattr(self, "Meta") and hasattr(self.Meta, "fields"):
                    if isinstance(self.Meta.fields, tuple):
                        self.Meta.fields = list(self.Meta.fields)
                    self.Meta.fields.append(resolved_field_name)

                # print(
                #     f"We will be creating a resolved field for field {field_name}. "
                #     f"Field is already custom-declared: {bool(s_field)}"
                # )
                pass

        return super().get_uniqueness_extra_kwargs(field_names, declared_fields, extra_kwargs)

    # noinspection PyUnresolvedReferences
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
        if hasattr(self.Meta, "changed_flds"):
            import warnings

            warnings.warn(
                f"""
                {self.__class__.__module__}.{self.__class__.__name__}:
                changed_flds has been found to be a duplicate of DRF's extra_kwargs Meta member. Either use
                extra_kwargs or the preferred field = AutoGeneratedField(**kwargs) declaration.
                """,
                DeprecationWarning,
                stacklevel=6,
            )
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
        ordering = "id"
        try:
            ordering = view.pagination_class.ordering
        except:
            pass
        if ordering != "id":
            query_params = self.context["request"].query_params
            query_params._mutable = True
            query_params.pop("id", "")
            queryset = view.filter_queryset(queryset=view.get_queryset(), query_params=query_params)
            records = list(queryset.order_by(ordering))
            curr_index = records.index(obj)
            prev_id = None
            if curr_index > 0:
                prev_id = records[curr_index - 1].id

            return prev_id

        return ""

    # noinspection PyMethodMayBeStatic
    def get_df_prev_id(self, obj):
        try:
            if self.context["request"].META.get("HTTP_X_DF_CALLTYPE", "") == "refresh_record":
                view = self.context.get("view", None)
                if view:
                    return self.fetch_prev_id(obj, view)
        except:
            pass

        return ""

    def render_to_table(self, value, row_data):
        return str(value) if value is not None else None


class Serializer(DynamicFormsSerializer, serializers.Serializer):
    def update(self, instance, validated_data):
        # Implemented just so IDE doesn't complain. Normally this will be handled in SingleRecordViewSet
        pass

    def create(self, validated_data):
        # Implemented just so IDE doesn't complain. Normally this will be handled in SingleRecordViewSet
        pass


class DynamicModelMixin:
    MODEL_FUNC_SETTING_NAME = None

    @staticmethod
    def determine_model_at_runtime_static(request, viewset=None, func_name=None):
        """
        Determines what model should be the basis for the serializer at runtime. Allows for dynamic model adjustments
        based on active code at the time of serialization
        :return:
        """
        if not func_name and viewset:
            func_name = getattr(settings, viewset.MODEL_FUNC_SETTING_NAME, None)
        if request and func_name:
            try:
                model_func = import_string(func_name)
                return model_func(viewset, request)
            except ImportError:
                pass
        return None

    def determine_model_at_runtime(self, request) -> Optional[models.Model]:
        return self.determine_model_at_runtime_static(request, self)


class DynamicModelSerializerMixin(DynamicModelMixin):
    LAYOUT_FUNC_SETTING_NAME = None

    def __init__(self, *args, **kwargs):
        if model := self.determine_model_at_runtime(kwargs.get("context", {}).get("request")):
            self.Meta.model = model
        super().__init__(*args, **kwargs)

    def determine_layout_at_runtime(self, request):
        """
        Determines what layout should be used for displaying the model at runtime. Allows for dynamic model adjustments
        based on active code at the time of serialization
        Usually you would override this like this:
          layout = self.Meta.layout.clone()
          layout.append_after_row('name_of_field', Row(...))
          return layout
        """
        try:
            layout_func = import_string(getattr(settings, self.LAYOUT_FUNC_SETTING_NAME, None))
            return layout_func(self, request)
        except ImportError:
            pass
        return self.Meta.layout
