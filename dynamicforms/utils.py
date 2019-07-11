from django.core.cache import cache


def get_progress_key(request):
    """
    Gets progress/operation key under which operation progress will be stored in servers cache.
    :param request:
    :return: Progress key or None if there is no x_df_timestamp in request header
    """
    timestamp = request.META.get('HTTP_X_DF_TIMESTAMP', request.GET.get('x_df_timestamp', None))
    if timestamp is not None:
        return '%s|%s' % (timestamp, request.session.session_key)
    return None


def set_progress_value(progress_key, value):
    """
    Updates operations progress

    :param progress_key: Key under which operations progress is stored
    :param value: Progress in percentages (0.00 - 1.00)
    :return:
    """
    if progress_key is not None:
        cache.set('df_progress.%s' % progress_key, value)
