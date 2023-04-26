import pathlib
import time
from typing import Optional
from uuid import uuid4

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext as __
from rest_framework import status
from rest_framework.exceptions import ValidationError

from dynamicforms.settings import DYNAMICFORMS

UPLOADED_FILE_NAME_TIMESTAMP_SEPARATOR = "_timestamp_"
UPLOADED_FILE_NAME_UUID_SEPARATOR = "_uuid_"
UPLOADED_FILE_TMP_LOCATION = "df_tmp_files"

preuploaded_fs = FileSystemStorage(location=f"{settings.MEDIA_ROOT}/{UPLOADED_FILE_TMP_LOCATION}")


def preupload_file(request):
    if not DYNAMICFORMS.allow_anonymous_user_to_preupload_files and not request.user.is_authenticated:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == "POST":
        uploaded_file: Optional[InMemoryUploadedFile] = request.FILES.get("file", None)
        if not uploaded_file:
            raise ValidationError(dict(file=["required"]))
        file_identifier: str = str(uuid4())
        try:
            file_extension: str = pathlib.Path(uploaded_file.name).suffix
            file_name: str = uploaded_file.name.replace(file_extension, "")
            preuploaded_fs.save(
                f"{file_name}{UPLOADED_FILE_NAME_UUID_SEPARATOR}{file_identifier}"
                f"{UPLOADED_FILE_NAME_TIMESTAMP_SEPARATOR}{int(time.time())}"
                f"{file_extension}",
                uploaded_file,
            )
            return JsonResponse(dict(identifier=file_identifier))
        except Exception:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, content=__("File upload failed").encode())
    return HttpResponse(status=status.HTTP_501_NOT_IMPLEMENTED)
