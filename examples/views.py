from django.shortcuts import redirect, render
from rest_framework.reverse import reverse

from .rest.basic_fields import BasicFields, BasicFieldsSerializer
from .rest.page_load import PageLoad, PageLoadSerializer

# Create your views here.
def index(request):
    return redirect(reverse('validated-list', args=['html']))


def view_mode(request):
    return render(request, "examples/view_mode.html", dict(
        page_data=BasicFieldsSerializer.get_component_context(request, BasicFields.objects.all()),
        # page_data = PageLoadSerializer.get_component_context(request, PageLoad.objects.all()),
    ))
