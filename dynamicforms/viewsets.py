from datetime import datetime, timedelta
from typing import List, Union

import pytz
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.db import models
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer, Serializer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from dynamicforms.action import FormButtonAction, FormButtonTypes
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
        return self.get_queryset().model()

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


class DeleteMixin(object):
    @action(detail=True, methods=['delete'])
    def confirm_delete(self: viewsets.ModelViewSet, request, *args, pk=None, format=None, **kwargs):
        record = self.get_object()
        serializer = self.get_serializer(record)
        confirm_delete_text = serializer.confirm_delete_text(request, self.get_object())
        if not confirm_delete_text:
            return self.destroy(request, *args, **kwargs)
        record_id = request.data.get('record_id')
        list_id = request.data.get('list_id')
        confirm_delete_button = FormButtonAction(
            btn_type=FormButtonTypes.CUSTOM, label=_('Confirm'), name='confirm',
            positions=['dialog'],
            button_is_primary=False,
            btn_classes=DYNAMICFORMS.form_button_classes + ' btn-danger {}'.format(
                "{}_{}".format(record_id, list_id)
            ))
        cancel_action = list(filter(lambda a: a.name == 'cancel', serializer.actions.actions))[0]
        serializer.actions.actions = []
        serializer.actions.actions.append(confirm_delete_button)
        serializer.actions.actions.append(cancel_action)
        render_data = dict(
            serializer=serializer,
            confirmation_text=confirm_delete_text,
            title=serializer.confirm_delete_title(),
        )
        return render(request,
                      DYNAMICFORMS.template + 'confirm_delete_dialog.html', render_data)


class CreateMixin(object):
    @action(detail=False, methods=['post'])
    def confirm_create(self: viewsets.ModelViewSet, request, *args, format=None, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.actions.actions.clear()
        serializer.actions.actions.append(
            FormButtonAction(btn_type=FormButtonTypes.SUBMIT, name='submit'))
        serializer.actions.actions.append(
            FormButtonAction(btn_type=FormButtonTypes.CANCEL, name='cancel'))
        serializer.is_valid(raise_exception=True)
        confirm_create = serializer.confirm_create_text()
        if not confirm_create:
            return self.create(request, *args, **kwargs)
        render_data = dict(
            serializer=serializer,
            confirmation_text=confirm_create,
            title=serializer.confirm_create_title(),
            url_reverse=self.template_context.get('url_reverse'),
        )
        return render(request, DYNAMICFORMS.template + 'confirm_create_dialog.html',
                      context=render_data, content_type=None, status=None, using=None)


class UpdateMixin(object):

    def remove_methods_fields_from_serializer(self, serializer_object: Serializer):
        fields_copy = serializer_object.fields.fields.copy()
        for field in fields_copy:
            f = fields_copy[field]
            if isinstance(f, SerializerMethodField):
                serializer_object.fields.fields.pop(field, None)

    @action(detail=True, methods=['put', 'patch'])
    def confirm_update(self: viewsets.ModelViewSet, request, *args, format=None, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.actions.actions.clear()
        serializer.actions.actions.append(
            FormButtonAction(btn_type=FormButtonTypes.SUBMIT, name='submit'))
        serializer.actions.actions.append(
            FormButtonAction(btn_type=FormButtonTypes.CANCEL, name='cancel'))
        serializer.is_valid(raise_exception=True)
        confirm_update = serializer.confirm_update_text()
        if not confirm_update:
            return self.update(request, *args, **kwargs)
        self.remove_methods_fields_from_serializer(serializer)
        render_data = dict(
            serializer=serializer,
            confirmation_text=confirm_update,
            title=serializer.confirm_update_title(),
            url_reverse=self.template_context.get('url_reverse'),
            instance_id=instance.pk
        )
        serializer.template_name = DYNAMICFORMS.template + 'base_form_confirm_update.html'
        return render(request, DYNAMICFORMS.template + 'confirm_create_dialog.html',
                      context=render_data, content_type=None, status=status.HTTP_403_FORBIDDEN, using=None)


class ReadOnlyMixin(object):
    @action(detail=True, methods=['get'])
    def view_readonly_detail(self: viewsets.ModelViewSet, request, pk=None, format=None):
        record = self.get_object()
        serializer = self.get_serializer(record, read_only_detail=True)
        return Response(serializer.data)


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

    e.g.

    .. code-block:: python

       template_context = lambda self: dict(items=MyModel.objects.all())

    or

    .. code-block:: python

       def template_context(self):
           return dict(items=MyModel.objects.all())
    """

    template_name = DYNAMICFORMS.table_base_template  #: template filename for listing multiple records (html renderer)

    # noinspection PyAttributeOutsideInit
    def initialize_request(self, request, *args, **kwargs):
        # Caution: just to be sure for any future debugging: the request parameter to this function is a WSGIRequest
        #  while the return Request is actually DRF Request
        #  As a consequence, form values don't get parsed until you actually call super().initialize_request
        #  There's no "request.data", etc. Just saying. So you don't debug for two hours next time. By "you" I mean me

        # Force render using a given render path (full page, table, table rows, form, dialog with form)
        self.render_type = request.META.get('HTTP_X_DF_RENDER_TYPE',
                                            request.GET.get('df_render_type', 'page'))

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
                return '?' + '&'.join(
                    ['%s=%s' % (key, value) for key, value in request.query_params.items()])
            return ''

        if isinstance(res.accepted_renderer, TemplateHTMLRenderer):
            if status.is_success(res.status_code) or res.status_code == status.HTTP_400_BAD_REQUEST:
                if request.method.lower() != 'delete':
                    if isinstance(res.data,
                                  dict) and 'next' in res.data and 'results' in res.data and \
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
                    else:
                        if isinstance(serializer, ListSerializer):
                            serializer.child.render_type = 'table'
                            serializer.child.data_template = self.template_name
                        else:
                            serializer.render_type = 'form'
                            serializer.data_template = serializer.template_name
                else:
                    # this is just faking data for rendering nothing in template, so that 204 goes through
                    from dynamicforms.serializers import Serializer
                    if not res.data:
                        serializer = Serializer({})
                        serializer.render_type = 'form'
                        serializer.data_template = DYNAMICFORMS.modal_dialog_template
                        res.data = serializer.data
                    else:
                        # faking if error would be 400
                        res.data.serializer.render_type = 'form'
                        res.data.serializer.data_template = DYNAMICFORMS.modal_dialog_template
            elif res.status_code == status.HTTP_401_UNAUTHORIZED and self.render_type != 'dialog':
                res = redirect_to_login(request.path_info + get_query_params())
            elif res.status_code == status.HTTP_403_FORBIDDEN:
                response_html = render(request,
                                       DYNAMICFORMS.template + 'exceptions/exception.html', dict(
                        detail=str(res.data.get('detail')),
                        title=_('Action denied')
                    ))
                response_html.status_code = status.HTTP_403_FORBIDDEN
                return response_html
            elif res.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                response_html = render(request,
                                       DYNAMICFORMS.template + 'exceptions/exception.html', dict(
                        detail=_('Please contact system administrator'),
                        title=getattr(res.exception, 'detail') if hasattr(
                            res, 'exception') and hasattr(res.exception, 'detail') else _('Unexpected error occured')
                    ))
                response_html.status_code = res.status_code
                return response_html
        return res

    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = super().get_exception_handler()

        context = super().get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None and isinstance(exc, Exception):
            # raise exception only for debug=True
            if settings.DEBUG or DYNAMICFORMS.api_debug:
                super().raise_uncaught_exception(exc)
            # if debug=False render html with error notification
            import logging
            logger = logging.getLogger('django.request')
            logger.exception(exc)
            response = Response(data={}, status=getattr(
                exc, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR))

        if response.status_code == status.HTTP_403_FORBIDDEN and hasattr(exc, 'args') and exc.args:
            response.data['detail'] = exc.args[0]

        response.exception = exc
        return response


class ModelViewSet(NewMixin, PutPostMixin, DeleteMixin, ReadOnlyMixin, CreateMixin, UpdateMixin,
                   TemplateRendererMixin,
                   viewsets.ModelViewSet):
    """
    In addition to all the functionality, provided by DRF, DynamicForms ViewSet has some extra features:

    * Separate templates for rendering list or single record
    * You can request a "new" record and even have it pre-populated with values
    * To render viewset as API or JSON use the same method as in DRF: To render it in HTML just add ".html" to the URL.
    * Standard DRF router URL patterns apply:

       * To render a new record use pk=new.
       * To render an existing record (for editing) use pk={record_id}.

    """

    def get_queryset(self):
        """
        Returns records from queryset with filters applied

        :return: filtered records
        """
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)

        return queryset.all()

    def filter_queryset(self, queryset):
        """
        Applies filters for all fields

        :param queryset: Queryset
        :return: queryset with filters applied
        """
        res = queryset
        for fld, val in self.request.query_params.items():
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
            for date_time_fmt in [settings.DATETIME_FORMAT, '%Y-%m-%dT%H:%M:%S',
                                  settings.DATE_FORMAT, '%Y-%m-%d']:
                try:
                    date_time = datetime.strptime(value, date_time_fmt)
                    break
                except:
                    pass
            if date_time is None:
                return queryset
            date_time = pytz.timezone(settings.TIME_ZONE).localize(date_time).astimezone(pytz.utc)
            if len(value) <= 10:
                return queryset.filter(
                    **{field + '__gte': date_time, field + '__lt': date_time + timedelta(days=1)})
            return queryset.filter(
                **{field + '__gte': date_time, field + '__lt': date_time + timedelta(seconds=1)})
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

        return MyCursorPagination

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            instance = self.new_object()
            ser = self.get_serializer(instance, data=request.data, partial=False)
            ser.is_valid(raise_exception=False)
            e.detail.serializer = ser
            raise e


class SingleRecordViewSet(NewMixin, TemplateRendererMixin, viewsets.GenericViewSet):

    def new_object(self):
        raise NotImplementedError()

    def create(self, request, *args, **kwargs):
        raise NotImplementedError()


# noinspection PyUnresolvedReferences
class GenericViewSet(NewMixin, PutPostMixin, TemplateRendererMixin, viewsets.GenericViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
