from django.conf.urls import include, url

from examples.rest import router
from .views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^dynamicforms/', include('dynamicforms.urls')),
]

from rest_framework.documentation import include_docs_urls
urlpatterns.append(
    url(r'^api-docs/', include_docs_urls(title='Example API documentation'))
)
