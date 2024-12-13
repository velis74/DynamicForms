from django.urls import re_path

from dynamicforms import preupload_files, progress

urlpatterns = [
    # Progress is used for checking on progress of operation on server
    re_path(r"^progress/$", progress.get_progress_value, name="progress"),
    re_path(r"^preupload-file/(?P<file_identifier>[\w-]+/)?$", preupload_files.FileUploadView.as_view(), name="preupload-file"),
]
