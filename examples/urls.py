from examples.rest import router
from django.conf.urls import url, include
from .views import index
from dynamicforms.settings import version_check
import rest_framework

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^', include(router.urls)),
]

# noinspection PyUnresolvedReferences
if version_check(rest_framework.VERSION, '3.7.0'):
    # noinspection PyUnresolvedReferences
    from rest_framework.documentation import include_docs_urls
    urlpatterns.append(
        url(r'^api-docs/', include_docs_urls(title='Example API documentation'))
    )
