from django.conf.urls import include
from django.urls import re_path
from rest_framework.documentation import include_docs_urls

from examples.rest import router
from .views import index

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^', include(router.urls)),
    re_path(r'^dynamicforms/', include('dynamicforms_legacy.urls')),
    re_path(r'^api-docs/', include_docs_urls(title='Example API documentation')),
]
