from django.shortcuts import redirect, render
from rest_framework.reverse import reverse

from .models import PageLoad
from .rest.page_load import PageLoadSerializer


# Create your views here.
def index(request):
    return redirect(reverse('validated-list', args=['html']))


def view_mode(request):
    return render(request, "examples/view_mode.html", dict(
        page_data=PageLoadSerializer.get_component_context(request, PageLoad.objects.all())
    ))
