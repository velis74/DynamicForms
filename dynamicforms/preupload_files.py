import time

from dataclasses import asdict, dataclass
from typing import Optional
from uuid import uuid4

from django.core.cache import cache
from django.utils.translation import gettext as __
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

# Cache constants
CACHE_EXPIRATION = 60 * 60  # 60 minutes
CACHE_KEY_PREFIX = "file_upload_"


@dataclass
class CachedFile:
    content: bytes
    name: str
    content_type: str
    size: int
    user_id: int
    timestamp: int

    @property
    def age_in_seconds(self) -> int:
        return int(time.time()) - self.timestamp


def count_user_cached_files(user_id: int) -> int:
    """Vrne število vseh cached datotek za uporabnika"""
    count = 0

    if hasattr(cache, "keys"):  # we expect redis in production
        for key in cache.keys(f"{CACHE_KEY_PREFIX}*"):
            file_data = cache.get(key)
            if file_data and file_data.get("user_id") == user_id:
                count += 1

    return count


class FileUploadView(APIView):
    def post(self, request):
        """Upload file to cache storage"""
        MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB
        MAX_FILES_PER_USER = 10

        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            raise ValidationError({"file": ["required"]})

        if uploaded_file.size > MAX_FILE_SIZE:
            msg = __("File size exceeds allowed maximum size of {size_mb}MB")
            raise ValidationError({"file": [msg.format(size_mb=MAX_FILE_SIZE // (1024 * 1024))]})

        user_id = request.user.id or -1

        if count_user_cached_files(user_id) >= MAX_FILES_PER_USER:
            raise ValidationError({"file": [__("Too many files uploaded. Please submit a form or try again later.")]})

        try:
            file_identifier = str(uuid4())
            file_content = uploaded_file.read()

            cached_file = CachedFile(
                content=file_content,
                name=uploaded_file.name,
                content_type=uploaded_file.content_type,
                size=uploaded_file.size,
                user_id=user_id,
                timestamp=int(time.time()),
            )

            cache_key = f"{CACHE_KEY_PREFIX}{file_identifier}"
            cache.set(cache_key, asdict(cached_file), CACHE_EXPIRATION)

            return Response({"identifier": file_identifier})

        except Exception as e:
            # V produkciji uporabi proper logging
            print(f"Error during file upload: {str(e)}")
            return Response({"error": __("File upload failed")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, file_identifier=None):
        """Delete file from cache storage"""
        if not file_identifier:
            raise ValidationError({"file_identifier": ["required"]})

        file_identifier = file_identifier.rstrip("/")  # remove the trailing slash
        cached_file = get_cached_file(file_identifier, request.user.id or -1)
        if not cached_file:
            raise NotFound(__("File not found"))

        cache_key = f"{CACHE_KEY_PREFIX}{file_identifier}"
        cache.delete(cache_key)

        return Response(status=status.HTTP_204_NO_CONTENT)


def get_cached_file(file_identifier: str, user_id: int, delete_from_cache: bool = False) -> Optional[CachedFile]:
    """Helper function to retrieve file from cache"""
    cache_key = f"{CACHE_KEY_PREFIX}{file_identifier}"
    file_data = cache.get(cache_key)

    if not file_data:
        return None

    if file_data.get("user_id") != user_id:
        raise PermissionDenied(__("You don't have permission to access this file"))

    if delete_from_cache:
        cache.delete(cache_key)

    return CachedFile(**file_data)
