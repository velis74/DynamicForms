import glob
import os
import pathlib
import time

from django.core.management.base import BaseCommand

from dynamicforms.preupload_files import preuploaded_fs, UPLOADED_FILE_NAME_TIMESTAMP_SEPARATOR
from dynamicforms.settings import DYNAMICFORMS


class Command(BaseCommand):
    help = "Clean old temporary files which are generated when preloading files for df preloaded file field"

    def handle(self, *args, **options):
        current_timestamp: int = int(time.time())
        margins_for_file_deletion: int = DYNAMICFORMS.preuploaded_file_margin_for_file_deletion_in_seconds
        for file in glob.glob(f"{preuploaded_fs.location}/*"):
            file_components: list = file.split(UPLOADED_FILE_NAME_TIMESTAMP_SEPARATOR)
            if len(file_components) > 1:
                file_path: pathlib.Path = pathlib.Path(file_components[1])
                timestamp: int = int(file_path.stem)
                if current_timestamp - timestamp > margins_for_file_deletion:
                    os.remove(file)
