from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from .rest import router


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-docs/', include_docs_urls(title='Example API documentation'))
]
