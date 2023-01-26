from django.conf.urls import include
from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog
from rest_framework.documentation import include_docs_urls

from examples.rest import router
from .views import component_index, index

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^component$', component_index, name='component_index'),
    re_path(r'^', include(router.urls)),
    re_path(r'^dynamicforms/', include('dynamicforms.urls')),
    re_path(r'^api-docs/', include_docs_urls(title='Example API documentation')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
