from django.shortcuts import redirect, render
from rest_framework.reverse import reverse

from dynamicforms.settings import DYNAMICFORMS
from .rest.basic_fields import BasicFields, BasicFieldsSerializer


# Create your views here.
def index(request):
    return redirect(reverse('validated-list', args=['component' if DYNAMICFORMS.components else 'html']))


def view_mode(request):
    return render(request, "examples/view_mode.html", dict(
        serializer=BasicFieldsSerializer.get_component_context(request, BasicFields.objects.all()),
        # page_data = PageLoadSerializer.get_component_context(request, PageLoad.objects.all()),
    ))
