from examples.rest import router
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from .views import index


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^api-docs/', include_docs_urls(title='Example API documentation'))
]
