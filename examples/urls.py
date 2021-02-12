from django.conf.urls import include, url
from rest_framework.documentation import include_docs_urls

from examples.rest import router
from .views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^dynamicforms/', include('dynamicforms.urls')),
    url(r'^api-docs/', include_docs_urls(title='Example API documentation')),
]
