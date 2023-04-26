from django.urls import re_path

from dynamicforms_legacy import progress

urlpatterns = [
    # Progress is used for checking on progress of operation on server
    re_path(r"^progress-legacy/$", progress.get_progress_value, name="progress"),
]
