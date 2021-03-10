from django.shortcuts import redirect, render
from rest_framework.reverse import reverse

from dynamicforms.template_render import ViewModeListSerializer
from .models import PageLoad
from .rest.page_load import PageLoadSerializer


# Create your views here.
def index(request):
    return redirect(reverse('validated-list', args=['html']))


def view_mode(request):
    # TODO: get a serializer up & running
    ser = PageLoadSerializer(
        PageLoad.objects.all(),
        view_mode_list=ViewModeListSerializer.ViewMode.TABLE,
        many=True
    )
    return render(request, "examples/view_mode.html", dict(page_data=ser))
