from django.shortcuts import redirect, render
from rest_framework.reverse import reverse

from dynamicforms.settings import DYNAMICFORMS
from .rest.basic_fields import BasicFields, BasicFieldsSerializer


# Create your views here.
def index(request):
    return redirect(reverse('validated-list', args=['component' if DYNAMICFORMS.components else 'html']))
