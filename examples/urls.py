from django.conf.urls import include, url
from django.urls import path
from rest_framework.documentation import include_docs_urls
from django.views.i18n import JavaScriptCatalog
from examples.rest import router
from .views import index, view_mode

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^view-mode$', view_mode, name='view-mode'),
    url(r'^', include(router.urls)),
    url(r'^dynamicforms/', include('dynamicforms.urls')),
    url(r'^api-docs/', include_docs_urls(title='Example API documentation')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
