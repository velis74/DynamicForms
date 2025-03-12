from django.conf.urls import include
from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from examples.rest import router

urlpatterns = [
    re_path(r"^", include(router.urls)),
    re_path(r"^dynamicforms/", include("dynamicforms.urls")),
    re_path(r"^api-schema/", SpectacularAPIView.as_view(), name="schema"),
    re_path(r"^api-docs/", SpectacularRedocView.as_view(url_name="schema")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
]
