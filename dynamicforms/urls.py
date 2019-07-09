from django.conf.urls import url
from dynamicforms import views

urlpatterns = [
    # Progress is used for checking on progress of operation on server
    url(r'^progress/$', views.get_progress_value, name='progress'),
]
