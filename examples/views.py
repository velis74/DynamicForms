from django.shortcuts import redirect, render
from rest_framework.request import Request
from rest_framework.reverse import reverse

from dynamicforms.filters import FilterBackend
from dynamicforms.template_render import ViewModeListSerializer, ViewModeSerializer
from dynamicforms.viewsets import ModelViewSet
from .models import PageLoad
from .rest.page_load import PageLoadSerializer


# Create your views here.
def index(request):
    return redirect(reverse('validated-list', args=['html']))


class FakeViewSet(object):
    """
    We fake a DRF ViewSet here to get ordering and pagination to work
    """
    def __init__(self, request, queryset):
        self.filter_backend = FilterBackend()
        self.request = request
        self.queryset = queryset

    @property
    def ordering(self):
        return self.filter_backend.get_ordering(self.request, self.queryset, None)


def view_mode(request):
    # TODO: this will probably become a helper method accepting queryset, serializer and optional paginator

    paginator = ModelViewSet.generate_paged_loader()()
    queryset = PageLoad.objects.all()

    # first we try to paginate the queryset, together with some sort ordering & stuff
    req = Request(request)
    req.accepted_renderer = None  # viewsets.py->MyCursorPagination.encode_cursor
    viewset = FakeViewSet(req, queryset)
    page = paginator.paginate_queryset(queryset, req)
    if page is None:
        # if unsuccessful, just resume with the entire queryset
        page = queryset

    ser = PageLoadSerializer(
        page,
        view_mode=ViewModeSerializer.ViewMode.TABLE_ROW,
        view_mode_list=ViewModeListSerializer.ViewMode.TABLE,
        context=dict(view=viewset),
        many=True
    )
    return render(request, "examples/view_mode.html", dict(page_data=ser))
