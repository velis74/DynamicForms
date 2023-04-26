from django.urls import re_path

from dynamicforms import preupload_files, progress

urlpatterns = [
    # Progress is used for checking on progress of operation on server
    re_path(r"^progress/$", progress.get_progress_value, name="progress"),
    re_path(r"^preupload-file/$", preupload_files.preupload_file, name="preupload-file"),
]
