import rest_framework
from django.conf.urls import include, url

from dynamicforms.settings import version_check
from examples.rest import router
from .views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^dynamicforms/', include('dynamicforms.urls')),
]

# noinspection PyUnresolvedReferences
if version_check(rest_framework.VERSION, '3.7.0'):
    # noinspection PyUnresolvedReferences
    from rest_framework.documentation import include_docs_urls
    urlpatterns.append(
        url(r'^api-docs/', include_docs_urls(title='Example API documentation'))
    )
