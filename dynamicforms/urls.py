from django.conf.urls import url

from dynamicforms import progress

urlpatterns = [
    # Progress is used for checking on progress of operation on server
    url(r'^progress/$', progress.get_progress_value, name='progress'),
]
