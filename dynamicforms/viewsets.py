from datetime import datetime, timedelta
from typing import List, Union

import pytz

from django.conf import settings
from django.db import models
from django.db.models import ProtectedError, RestrictedError
from django.http import Http404
from django.utils.dateparse import (
    datetime_re,
    iso8601_duration_re,
    parse_datetime,
    parse_duration,
    parse_time,
    standard_duration_re,
    time_re,
)
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer

from dynamicforms.fields import BooleanField
from dynamicforms.utils import get_pk_name


class NewMixin:
    """
    Provides support for retrieving default values for a new record.

    Caution: Do not use directly. This is only a mixin and is used in final ViewSet derivatives.
    """

    def get_object(self: viewsets.ModelViewSet):
        """
        Returns the new_object if "new" is requested, otherwise from database
        """
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if (
            # "new" was requested directly
            (lookup_url_kwarg in self.kwargs and self.kwargs[lookup_url_kwarg] == "new")
            or
            # if this is a SingleRecordViewSet, our router may have created routes where pk won't even be there
            (lookup_url_kwarg not in self.kwargs and isinstance(self, SingleRecordViewSet))
        ):
            return self.new_object()

        return super().get_object()

    def new_object(self: viewsets.ModelViewSet):
        """
        Returns a new model instance. If you need it pre-populated with default values, this is the method to override.

        :return: model instance
        """
        # TODO: This function must return an object that has its field values correctly / realistically filled out
        #  Example: if a certain field's value hides (sets another field to None), then that second field can't be
        #  set to 42, can it?
        #  can we run some kind of validation to enforce this?
        #  Not that easy: the returned record may not validate for its (correctly) empty fields
        #  Maybe we will have to run JavaScript onchange for all fields displayed to ensure at least some consistency?
        #  If we do not, subsequent validation may fail because a hidden field has a value
        field_names = [
            (f.name + "_id") if isinstance(f, models.ForeignKey) else f.name
            for f in self.get_queryset().model._meta.fields
        ]
        model = self.get_queryset().model
        fld = model._meta.get_field
        instantiation_params = {k: fld(k).to_python(v) for k, v in self.request.GET.items() if k in field_names}
        return self.get_queryset().model(**instantiation_params)

    # noinspection PyUnresolvedReferences
    def retrieve(self: viewsets.ModelViewSet, request, *args, **kwargs):
        try:
            if not hasattr(super(), "retrieve"):
                raise Http404()  # This is not a ModelViewSet, so we don't have a retrieval mechanism
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            filter_kwargs = {
                self.lookup_field: self.kwargs.get(
                    # if this is a SingleRecordViewSet, our router may have created routes where pk won't even be there
                    lookup_url_kwarg,
                    "new" if isinstance(self, SingleRecordViewSet) else None,
                )
            }
            if filter_kwargs.get(self.lookup_field, None) == "new":
                instance = self.new_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise


class PutPostMixin(object):
    """
    Provides support for when there is no record id in URL when calling PUT
    (First empty form is loaded. Then user loads existing data to this form and updates it... - Perform PUT action)

    or

    Provides support for when there is record id in URL when calling POST
    (First form for some existing record is loaded. Then user wants to create new record for it.
    - deletes record ID and perform POST action)
    """

    # When there is no record id in URL when calling PUT, this function will be called
    # noinspection PyUnresolvedReferences
    def put(self: viewsets.ModelViewSet, request, *args, **kwargs):
        self.kwargs["pk"] = request.data[get_pk_name(self.get_queryset())]
        return self.update(request, *args, **kwargs)

    # When there is record id in URL when calling POST, this function will be called
    # noinspection PyUnresolvedReferences
    def post(self: viewsets.ModelViewSet, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TemplateRendererMixin:
    template_context = {}
    """
    template_context provides configuration to templates being rendered

    Note that when adding data from database, it is advised to make this definition a callable so that it is evaluated
    on each render of the ViewSet: that way you can ensure data is always loaded fresh from database.
    This member can also be defined in the serializer class. If that is the case, it will be copied to ViewSet.

    e.g.

    .. code-block:: python

       template_context = lambda self: dict(items=MyModel.objects.all())

    or

    .. code-block:: python

       def template_context(self):
           return dict(items=MyModel.objects.all())
    """

    def __init__(self, *args, **kwds):
        if not self.template_context and getattr(self, "serializer_class", None) is not None:
            self.template_context = getattr(self.serializer_class, "template_context", {})
        super().__init__(*args, **kwds)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        if self.format_kwarg == "component":
            # view_mode support: set viewmode when DRF renderer is the component renderer
            if isinstance(serializer, ListSerializer):
                serializer.apply_component_context(self.request, self.paginator)
            else:
                serializer.apply_component_context(self.request, None)
        return serializer

    # noinspection PyAttributeOutsideInit
    def initialize_request(self, request, *args, **kwargs):
        # Caution: just to be sure for any future debugging: the request parameter to this function is a WSGIRequest
        #  while the return Request is actually DRF Request
        #  As a consequence, form values don't get parsed until you actually call super().initialize_request
        #  There's no "request.data", etc. Just saying. So you don't debug for two hours next time. By "you" I mean me

        # Force render using a given render path (full page, table, table rows, form, dialog with form)
        self.render_type = request.META.get("HTTP_X_DF_RENDER_TYPE", request.GET.get("df_render_type", "page"))

        if request.method.lower() == "post" and request.POST.get("data-dynamicforms-method", None):
            # This is a hack because HTML forms can only do POST & GET. This way we also get PUT & PATCH
            request.method = request.POST.get("data-dynamicforms-method")
            # If we don't set this META, django won't recognise our CSRF token
            request.META["HTTP_X_CSRFTOKEN"] = request.POST["csrfmiddlewaretoken"]
        return super().initialize_request(request, *args, **kwargs)


class ModelViewSet(NewMixin, PutPostMixin, TemplateRendererMixin, viewsets.ModelViewSet):
    """
    In addition to all the functionality, provided by DRF, DynamicForms ViewSet has some extra features:

    * Separate templates for rendering list or single record
    * You can request a "new" record and even have it pre-populated with values
    * To render viewset as API or JSON use the same method as in DRF: To render it in HTML just add ".html" to the URL.
    * Standard DRF router URL patterns apply:

       * To render a new record use pk=new.
       * To render an existing record (for editing) use pk={record_id}.

    """

    ordering_parameter = "ordering"
    ordering_style = None

    @property
    def paginator(self):
        if self.request:
            request = self.request
            pagination_enabled = request.META.get("HTTP_X_PAGINATION", request.GET.get("x_df_pagination", False))
            pagination_enabled = BooleanField().to_internal_value(pagination_enabled)
            if isinstance(request.accepted_renderer, JSONRenderer) and not pagination_enabled:
                # if pagination is disabled, we need to hide the paginator so that nothing breaks looking for it
                return None
        return super().paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_queryset(self):
        """
        Returns records from queryset with filters applied

        :return: filtered records
        """
        return super().get_queryset()

    def filter_queryset(self, queryset, query_params=None):
        """
        Applies filters for all fields

        :param queryset: Queryset
        :param query_params: Custom query_params if needed
        :return: queryset with filters applied
        """
        res = super().filter_queryset(queryset)
        if self.request:
            if query_params is None:
                query_params = self.request.query_params
            for fld, val in query_params.items():
                res = self.filter_queryset_field(res, fld, val)
            for backend in self.filter_backends:
                if hasattr(backend, "get_ordering"):
                    ordering = backend().get_ordering(self.request, queryset, self)
                    if ordering:
                        self.ordering = ordering
                        break
        return res

    def __get_time_resolution(self, value: str) -> dict:
        try:
            value = value.replace("Z", "")
            resolution = (
                getattr(time_re.match(value), "lastgroup", "")
                or getattr(datetime_re.match(value), "lastgroup", "")
                or getattr(standard_duration_re.match(value), "lastgroup", "")
                or getattr(iso8601_duration_re.match(value), "lastgroup", "")
            )
            if resolution in ("second", "microsecond", "seconds", "microseconds"):
                return dict(seconds=1)
            if resolution in ("hour", "hours"):
                return dict(hours=1)
            if resolution in ("minute", "minutes"):
                return dict(minutes=1)
        except:
            pass
        return {}

    # noinspection PyMethodMayBeStatic
    def filter_queryset_field(self, queryset, field, value):
        """
        Applies filter to individual field

        :param queryset: Queryset
        :param field: Field name
        :param value: Field value
        :return: queryset with applied filter for the field
        """
        if value is None or value == "":
            return queryset

        model_meta = queryset.model._meta

        if field not in (fld.name for fld in model_meta.get_fields()):
            return queryset

        try:
            # TODO: this would probably be better moved into the fields themselves
            if isinstance(model_meta.get_field(field), (models.CharField, models.TextField)):
                return queryset.filter(**{field + "__icontains": value})
            if isinstance(model_meta.get_field(field), (models.DateTimeField,)):
                date_time: datetime = parse_datetime(value.replace("Z", ""))
                date_time.replace(microsecond=0)
                date_time = pytz.timezone(settings.TIME_ZONE).localize(date_time).astimezone(pytz.utc)
                return queryset.filter(
                    **{
                        field + "__gte": date_time,
                        field + "__lt": date_time + timedelta(**self.__get_time_resolution(value)),
                    }
                )
            if isinstance(model_meta.get_field(field), (models.TimeField,)):
                start = datetime.combine(datetime.now().date(), parse_time(value).replace(microsecond=0))
                end = (start + timedelta(**self.__get_time_resolution(value))).time()
                return queryset.filter(**{field + "__gte": start, field + "__lt": end})
            if isinstance(model_meta.get_field(field), (models.DurationField,)):
                duration = parse_duration(value)
                duration = duration - timedelta(microseconds=duration.microseconds)
                return queryset.filter(
                    **{
                        field + "__gte": duration,
                        field + "__lt": duration + timedelta(**self.__get_time_resolution(value)),
                    }
                )
            if isinstance(model_meta.get_field(field), (models.DateField,)):
                date_time = None
                for date_time_fmt in [settings.DATE_FORMAT, "%Y-%m-%d"]:
                    try:
                        date_time = datetime.strptime(value, date_time_fmt)
                        break
                    except:
                        pass
                date_time = pytz.timezone(settings.TIME_ZONE).localize(date_time).astimezone(pytz.utc)
                return queryset.filter(**{field + "__gte": date_time, field + "__lt": date_time + timedelta(days=1)})
            else:
                if isinstance(model_meta.get_field(field), models.BooleanField):
                    value = value == "true"
                return queryset.filter(**{field: value})
        except:
            return queryset

    @staticmethod
    def generate_paged_loader(page_size: int = 30, ordering: Union[str, List[str]] = "id"):
        """
        Generates a Pagination class that will handle dynamic data loading for ViewSets with a lot of data.
        Use by declaring `pagination_class = ModelViewSet.generate_paged_loader()` in class variables

        :param page_size: how many records should be fetched at a time
        :param ordering: This should be a string, or list of strings, indicating the field against which the cursor
           based pagination will be applied. For example: ordering = 'slug'
        :return: a Pagination class
        """
        from dynamicforms.pagination import CursorPagination

        ps = page_size
        ordr = ordering

        class MyCursorPagination(CursorPagination):
            ordering = ordr
            page_size = ps
            df_request = None

            def paginate_queryset(self, queryset, request, view=None):
                self.df_request = request
                return super().paginate_queryset(queryset, request, view)

            def encode_cursor(self, cursor):
                # Following code is needed when we have https proxy server that redirects requests to http servers.
                # In that case original code generates cursor links that have http scheme.
                # So here I check REFERER header to find out which scheme is originally declared.
                # And use that one in cursor link.
                request = getattr(self, "df_request", None)
                cursor_url = super().encode_cursor(cursor).split(":", 1)
                req_url = self.df_request.META.get("HTTP_REFERER", None)
                if req_url:
                    req_url = req_url.split(":", 1)
                    if cursor_url[0] != req_url[0] and req_url[0].lower() in ("http", "https"):
                        cursor_url[0] = req_url[0]
                cursor_url = ":".join(cursor_url)
                if (
                    request
                    and isinstance(request.accepted_renderer, JSONRenderer)
                    and "x_df_pagination" not in cursor_url
                ):
                    cursor_url += "&x_df_pagination=1"
                return cursor_url

            def get_paginated_response(self, data):
                # TODO: this is to be removed - we're getting component definitions through
                #  ComponentHTMLRenderer.render_type=component-def
                serializer = data.serializer
                request = serializer.request
                if (
                    request
                    and isinstance(request.accepted_renderer, JSONRenderer)
                    and BooleanField().to_internal_value(request.META.get("HTTP_X_DF_COMPONENT_DEF", False))
                ):
                    # if component definition was requested, let's return that and not just the data
                    serializer.apply_component_context(request, self)
                    return Response(
                        serializer.component_params(
                            output_json=False,
                            data=dict(next=self.get_next_link(), previous=self.get_previous_link(), results=data),
                        )
                    )
                return super().get_paginated_response(data)

        return MyCursorPagination

    def handle_create_validation_exception(self, e, request, *args, **kwargs):
        instance = self.new_object()
        ser = self.get_serializer(instance, data=request.data, partial=False)
        ser.is_valid(raise_exception=False)
        e.detail.serializer = ser
        raise e

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            self.handle_create_validation_exception(e, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except (ProtectedError, RestrictedError):
            return Response(_("Deletion not allowed: This record is linked to other records."), status=400)


class ViewSet(NewMixin, viewsets.ViewSet):
    # When using this class make sure you do a serializer.apply_component_context before returning Response(serializer)
    pass


class SingleRecordViewSet(NewMixin, TemplateRendererMixin, viewsets.GenericViewSet):
    def new_object(self):
        raise NotImplementedError()

    def create(self, request, *args, **kwargs):
        raise NotImplementedError()


# noinspection PyUnresolvedReferences
class GenericViewSet(NewMixin, PutPostMixin, TemplateRendererMixin, viewsets.GenericViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
