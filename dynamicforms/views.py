# from django.shortcuts import render

from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from dynamicforms.utils import get_progress_key


def get_progress_value(request):
    """
    Returns operations progress to client

    :param request:
    :return: Progress in percentages (0 - 100) if progress is set else None
    """
    progress_key = get_progress_key(request)
    value = None
    if progress_key is not None:
        cache_value = cache.get('df_progress.%s' % progress_key)
        if cache_value is not None:
            value = '%.2f' % (cache.get('df_progress.%s' % progress_key) * 100)
    return HttpResponse(JSONRenderer().render(dict(value=value)), content_type='application/json')
