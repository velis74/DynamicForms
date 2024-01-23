from django.conf.urls import include
from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog
from rest_framework.documentation import include_docs_urls

from examples.rest import router

urlpatterns = [
    re_path(r"^", include(router.urls)),
    re_path(r"^dynamicforms/", include("dynamicforms.urls")),
    re_path(r"^api-docs/", include_docs_urls(title="Example API documentation")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
]
