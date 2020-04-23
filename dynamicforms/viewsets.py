from datetime import datetime, timedelta
from typing import List, Union

import pytz
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.db import models
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from dynamicforms.fields import BooleanField
from .renderers import TemplateHTMLRenderer
from .settings import DYNAMICFORMS


class NewMixin(object):
    """
    Provides support for retrieving default values for a new record.

    Caution: Do not use directly. This is only a mixin and is used in final ViewSet derivatives.
    """

    def new_object(self: viewsets.ModelViewSet):
        """
        Returns a new model instance. If you need it pre-populated with default values, this is the method to override.

        :return: model instance
        """
        # TODO: This function must return an object that has its field values correctly / realistically filled out
        # Example: if a certain field's value hides (sets another field to None), then that second field can't be
        # set to 42, can it?
        # can we run some kind of validation to enforce this?
        # Not that easy: the returned record may not validate for its (correctly) empty fields
        # Maybe we will have to run JavaScript onchange for all fields displayed to ensure at least some consistency?
        # If we do not, subsequent validation may fail because a hidden field has a value
        field_names = [(f.name + '_id') if isinstance(f, models.ForeignKey) else f.name
                       for f in self.get_queryset().model._meta.fields]
        instantiation_params = {k: v for k, v in self.request.GET.items() if k in field_names}
        return self.get_queryset().model(**instantiation_params)

    # noinspection PyUnresolvedReferences
    def retrieve(self: viewsets.ModelViewSet, request, *args, **kwargs):
        try:
            if not hasattr(super(), 'retrieve'):
                raise Http404()  # This is not a ModelViewSet, so we don't have a retrieval mechanism
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            if filter_kwargs.get('pk', None) == 'new':
                instance = self.new_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise


class PutPostMixin(object):
    """
    Provides support for when there is no record id in URL when calling PUT
    (First empty form is loaded. Than user loads existing data to this form and updates it... - Perform PUT action)

    or

    Provides support for when there is record id in URL when calling POST
    (First form for some existing record is loaded. Than user wants to create new record for it.
    - deletes redord ID and perform POST action)
    """

    # When there is no record id in URL when calling PUT, this function will be called
    # noinspection PyUnresolvedReferences
    def put(self: viewsets.ModelViewSet, request, *args, **kwargs):
        self.kwargs['pk'] = request.data['id']
        return self.update(request, *args, **kwargs)

    # When there is record id in URL when calling POST, this function will be called
    # noinspection PyUnresolvedReferences
    def post(self: viewsets.ModelViewSet, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TemplateRendererMixin():
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

    template_name = DYNAMICFORMS.table_base_template  #: template filename for listing multiple records (html renderer)

    def __init__(self, *args, **kwds):
        if not self.template_context and getattr(self, 'serializer_class', None) is not None:
            self.template_context = getattr(self.serializer_class, 'template_context', {})
        super().__init__(*args, **kwds)

    # noinspection PyAttributeOutsideInit
    def initialize_request(self, request, *args, **kwargs):
        # Caution: just to be sure for any future debugging: the request parameter to this function is a WSGIRequest
        #  while the return Request is actually DRF Request
        #  As a consequence, form values don't get parsed until you actually call super().initialize_request
        #  There's no "request.data", etc. Just saying. So you don't debug for two hours next time. By "you" I mean me

        # Force render using a given render path (full page, table, table rows, form, dialog with form)
        self.render_type = request.META.get('HTTP_X_DF_RENDER_TYPE', request.GET.get('df_render_type', 'page'))

        if request.method.lower() == 'post' and request.POST.get('data-dynamicforms-method', None):
            # This is a hack because HTML forms can only do POST & GET. This way we also get PUT & PATCH
            request.method = request.POST.get('data-dynamicforms-method')
            # If we don't set this META, django won't recognise our CSRF token
            request.META['HTTP_X_CSRFTOKEN'] = request.POST['csrfmiddlewaretoken']
        return super().initialize_request(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        if not isinstance(response, Response):
            return response

        res = super().finalize_response(request, response, *args, **kwargs)

        def get_query_params():
            if request.query_params:
                return '?' + '&'.join(['%s=%s' % (key, value) for key, value in request.query_params.items()])
            return ''

        if isinstance(res.accepted_renderer, TemplateHTMLRenderer):
            if status.is_success(res.status_code) or res.status_code == status.HTTP_400_BAD_REQUEST:
                if isinstance(res.data, dict) and 'next' in res.data and 'results' in res.data and \
                        isinstance(res.data['results'], (ReturnList, ReturnDict)):
                    serializer = res.data['results'].serializer
                else:
                    serializer = res.data.serializer

                if isinstance(serializer, ListSerializer):
                    serializer.child.render_type = self.render_type
                else:
                    serializer.render_type = self.render_type

                if self.render_type in ('table', 'table rows'):
                    serializer.data_template = self.template_name
                elif self.render_type == 'dialog':
                    serializer.data_template = DYNAMICFORMS.modal_dialog_template
                    res.template_name = DYNAMICFORMS.modal_dialog_template
                elif self.render_type == 'form':
                    serializer.data_template = res.data.serializer.template_name
                    res.template_name = res.data.serializer.template_name
                else:
                    if isinstance(serializer, ListSerializer):
                        serializer.child.render_type = 'table'
                        serializer.child.data_template = self.template_name
                    else:
                        serializer.render_type = 'form'
                        serializer.data_template = serializer.template_name
            elif res.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN) and \
                    self.render_type != 'dialog':
                # TODO: We should show a message here that user is not authorized for this action (only for 403)
                res = redirect_to_login(request.path_info + get_query_params())
        return res


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

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        # determine request format and handle pagination for json format
        if isinstance(self.request.accepted_renderer, JSONRenderer) and not BooleanField().to_internal_value(
                self.request.META.get('HTTP_X_PAGINATION', self.request.GET.get('x_df_pagination', False))):
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
        res = queryset
        if self.request:
            if query_params is None:
                query_params = self.request.query_params
            for fld, val in query_params.items():
                res = self.filter_queryset_field(res, fld, val)
        return res

    # noinspection PyMethodMayBeStatic
    def filter_queryset_field(self, queryset, field, value):
        """
        Applies filter to individual field

        :param queryset: Queryset
        :param field: Field name
        :param value: Field value
        :return: queryset with applied filter for the field
        """
        if value is None or value == '':
            return queryset

        model_meta = queryset.model._meta

        if field not in (fld.name for fld in model_meta.get_fields()):
            return queryset

        # TODO: this would probably be better moved into the fields themselves
        if isinstance(model_meta.get_field(field), (models.CharField, models.TextField)):
            return queryset.filter(**{field + '__icontains': value})
        if isinstance(model_meta.get_field(field), (models.DateField, models.DateTimeField)):
            date_time = None
            for date_time_fmt in [settings.DATETIME_FORMAT, '%Y-%m-%dT%H:%M:%S', settings.DATE_FORMAT, '%Y-%m-%d']:
                try:
                    date_time = datetime.strptime(value, date_time_fmt)
                    break
                except:
                    pass
            if date_time is None:
                return queryset
            date_time = pytz.timezone(settings.TIME_ZONE).localize(date_time).astimezone(pytz.utc)
            if len(value) <= 10:
                return queryset.filter(**{field + '__gte': date_time, field + '__lt': date_time + timedelta(days=1)})
            return queryset.filter(**{field + '__gte': date_time, field + '__lt': date_time + timedelta(seconds=1)})
        else:
            if isinstance(model_meta.get_field(field), models.BooleanField):
                value = (value == 'true')
            return queryset.filter(**{field: value})

    @staticmethod
    def generate_paged_loader(page_size: int = 30, ordering: Union[str, List[str]] = 'id'):
        """
        Generates a Pagination class that will handle dynamic data loading for ViewSets with a lot of data.
        Use by declaring `pagination_class = ModelViewSet.generate_paged_loader()` in class variables

        :param page_size: how many records should be fetched at a time
        :param ordering: This should be a string, or list of strings, indicating the field against which the cursor
           based pagination will be applied. For example: ordering = 'slug'
        :return: a Pagination class
        """
        from rest_framework.pagination import CursorPagination
        ps = page_size
        ordr = ordering

        class MyCursorPagination(CursorPagination):
            ordering = ordr
            page_size = ps
            df_request = None

            def paginate_queryset(self, queryset, request, view=None):
                self.df_request = request
                return super().paginate_queryset(queryset, request, view=None)

            def encode_cursor(self, cursor):
                # Following code is needed when we have https proxy server that redirects requests to http servers.
                # In that case original code generates cursor links that have http scheme.
                # So here I check REFERER header to find out which scheme is originally declared.
                # And use that one in cursor link.
                request = getattr(self, 'df_request', None)
                cursor_url = super().encode_cursor(cursor).split(':', 1)
                req_url = self.df_request.META.get('HTTP_REFERER', None)
                if req_url:
                    req_url = req_url.split(':', 1)
                    if cursor_url[0] != req_url[0] and req_url[0].lower() in ('http', 'https'):
                        cursor_url[0] = req_url[0]
                cursor_url = ':'.join(cursor_url)
                if request and isinstance(request.accepted_renderer, JSONRenderer):
                    cursor_url += '&x_df_pagination=1'
                return cursor_url

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


class SingleRecordViewSet(NewMixin, TemplateRendererMixin, viewsets.GenericViewSet):

    def new_object(self):
        raise NotImplementedError()

    def create(self, request, *args, **kwargs):
        raise NotImplementedError()


# noinspection PyUnresolvedReferences
class GenericViewSet(NewMixin, PutPostMixin, TemplateRendererMixin, viewsets.GenericViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
