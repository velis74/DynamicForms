from django.shortcuts import redirect, render
from rest_framework.reverse import reverse

# Create your views here.
from dynamicforms.settings import DYNAMICFORMS
from examples.models import HiddenFields, AdvancedFields, RefreshType
from examples.rest.advanced_fields import AdvancedFieldsSerializer
from examples.rest.hidden_fields import HiddenFieldsSerializer
from examples.rest.refresh_types import RefreshTypesSerializer


def index(request):
    return redirect(reverse('validated-list', args=['html']))


def multiple_serializers_on_page(request):
    """
    Renders multiple serializers on page

    :param request: Request
    :return: Rendered view
    """
    hidden_fields_serializer = HiddenFieldsSerializer(
        HiddenFields.objects.all(),
        many=True, )
    hidden_fields_serializer.child.data_template = DYNAMICFORMS.table_base_template

    advanced_fields_serializer = AdvancedFieldsSerializer(
        AdvancedFields.objects.all(),
        many=True, )
    advanced_fields_serializer.child.data_template = DYNAMICFORMS.table_base_template

    refresh_types_serializer = RefreshTypesSerializer(
        RefreshType.objects.all(),
        many=True, )
    refresh_types_serializer.child.data_template = DYNAMICFORMS.table_base_template

    context = dict(
        DYNAMICFORMS=DYNAMICFORMS,
        tables_page_title='Multiple serializers rendered on one page',
        tables=dict(
            hidden_fields=dict(
                data=hidden_fields_serializer.data,
                serializer=hidden_fields_serializer.child,
                url_reverse='hidden-fields',
                title='Hidden fields',
            ),
            advanced_fields=dict(
                data=advanced_fields_serializer.data,
                serializer=advanced_fields_serializer.child,
                url_reverse='advanced-fields',
                title='Validated',
            ),
            refresh_type_fields=dict(
                data=refresh_types_serializer.data,
                serializer=refresh_types_serializer.child,
                url_reverse='refresh-types',
                title='Refresh types',
            ),
        )
    )
    return render(request, 'examples/page.html', context=context)
