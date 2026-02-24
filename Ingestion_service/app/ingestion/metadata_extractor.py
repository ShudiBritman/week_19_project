import os
from PIL import Image


class MetaDataExtractor:

    @staticmethod
    def extract_metadata(file_path):
        file_size = os.path.getsize(file_path)

        with Image.open(file_path) as img:
            width, height = img.size
            format_file = img.format

        metadata = {
            "file_size": file_size,
            "width": width,
            "height": height,
            "format_file": format_file
        }
        return metadata
