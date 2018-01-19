from django.shortcuts import render
from .forms import ValidatedForm
from .models import Validated


# Create your views here.
def validated(request):
    return render(request, 'examples/validated.html', dict(
        validated_tbl=ValidatedForm(initial=Validated.objects),  # This one should render into table
        validated_rec=ValidatedForm(initial=Validated.objects.first())  # This one should render into form
    ))
