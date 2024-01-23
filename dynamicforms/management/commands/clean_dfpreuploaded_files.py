import glob
import os
import pathlib
import time

from django.core.management.base import BaseCommand

from dynamicforms.preupload_files import preuploaded_fs, UPLOADED_FILE_NAME_TIMESTAMP_SEPARATOR


class Command(BaseCommand):
    # TODO: this is redundant: the files should not be uploaded to any persistent storage, but instead to cache
    #  with a really short timeout, max a few hours. After that, they're gone automatically. No need for a clean up
    #  script nobody ever thought to setup to run in the first place. Task DF:#873
    help = "Clean old temporary files which are generated when preloading files for df preloaded file field"

    def handle(self, *args, **options):
        current_timestamp: int = int(time.time())
        margins_for_file_deletion: int = 86400  # one day od uploaded file retention
        for file in glob.glob(f"{preuploaded_fs.location}/*"):
            file_components: list = file.split(UPLOADED_FILE_NAME_TIMESTAMP_SEPARATOR)
            if len(file_components) > 1:
                file_path: pathlib.Path = pathlib.Path(file_components[1])
                timestamp: int = int(file_path.stem)
                if current_timestamp - timestamp > margins_for_file_deletion:
                    os.remove(file)
