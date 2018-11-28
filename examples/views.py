from django.shortcuts import redirect
from rest_framework.reverse import reverse


# Create your views here.
def index(request):
    return redirect(reverse('validated-list', args=['html']))
