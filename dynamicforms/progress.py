from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


def get_progress_value(request):
    """
    Returns operations progress to HTTP client

    :param request:
    :return: Progress in percentages (0 - 100) if progress is set else None
    """
    progress_key = get_progress_key(request)
    value = None
    if progress_key is not None:
        cache_value = cache.get("df_progress.%s" % progress_key)
        if cache_value is not None:
            value = "%.2f" % cache.get("df_progress.%s" % progress_key)

    return HttpResponse(
        JSONRenderer().render(dict(value=value, comment=cache.get("df_progress_comment.%s" % progress_key))),
        content_type="application/json",
    )


def get_progress_key(request):
    """
    Gets progress/operation key under which operation progress will be stored in servers cache.
    :param request:
    :return: Progress key or None if there is no x_df_timestamp in request header
    """
    timestamp = request.META.get("HTTP_X_DF_TIMESTAMP", request.GET.get("x_df_timestamp", None))
    if timestamp is not None:
        return "%s|%s" % (timestamp, request.session.session_key)
    return None


def set_progress_value(progress_key, value):
    """
    Updates operations progress

    :param progress_key: Key under which operations progress is stored
    :param value: Progress in percentages (0.00 - 100.00)
    :return:
    """
    if progress_key is not None:
        cache.set("df_progress.%s" % progress_key, value)


def add_progress_value(progress_key, value):
    """
    Updates operations progress by adding to existing progress value

    :param progress_key: Key under which operations progress is stored
    :param value: Progress in percentages (0.00 - 100.00)
    :return:
    """
    if progress_key is not None:
        cache.set("df_progress.%s" % progress_key, cache.get("df_progress.%s" % progress_key, 0) + value)


def set_progress_comment(progress_key, value):
    """
    Updates operations comment

    :param progress_key: Key under which operations progress is stored
    :param value: comment
    :return:
    """
    if progress_key is not None:
        cache.set("df_progress_comment.%s" % progress_key, value)
