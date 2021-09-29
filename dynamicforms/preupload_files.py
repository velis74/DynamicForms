from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


# @login_required
def preupload_file(request):
    a = 9
    if request.method == 'POST':
        s = 9
    return HttpResponse('successfully uploaded')