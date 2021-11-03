from django.conf.urls import url

from dynamicforms import preupload_files, progress

urlpatterns = [
    # Progress is used for checking on progress of operation on server
    url(r'^progress/$', progress.get_progress_value, name='progress'),
    url(r'^preupload-file/$', preupload_files.preupload_file, name='preupload-file'),
]
