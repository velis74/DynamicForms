from django.shortcuts import redirect, render
from rest_framework.reverse import reverse

from dynamicforms.settings import DYNAMICFORMS


# Create your views here.
def index(request):
    return redirect(reverse('validated-list', args=['component' if DYNAMICFORMS.components else 'html']))


def component_index(request):
    DYNAMICFORMS.components = True
    try:
        return render(request, 'examples/component_index.html')
    finally:
        DYNAMICFORMS.components = False
