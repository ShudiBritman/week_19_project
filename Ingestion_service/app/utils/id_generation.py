from uuid import uuid4
from pathlib import Path
import requests
import os
from app.logger.logger import get_logger

logger = get_logger("request")

class IdGeneration:

    @staticmethod
    def add_id(file_path):
        file_path = Path(file_path)
        details = {
            'id': str(uuid4()),
            'filename': file_path.name,
            'file_path': file_path
        }
        return details
    


def build_event(image_id, metadata, image_text):
    event = {
        'id': image_id,
        'meta_data': metadata,
        'image_text': image_text
    }
    return event


def build_http_request(image_path):

    host = os.getenv('MONGO_LOADER_HOST')
    port = os.getenv('MONGO_LOADER_PORT')

    url = f"http://{host}:{port}/load_image"

    with open(image_path, "rb") as f:
        files = {"binary_file": f}

        logger.info("Sending to: %s", url)

        response = requests.post(url, files=files)

        logger.info("Status: %s", response.status_code)
        logger.info("Response: %s", response.text)
        return {"status":response.status_code, "response": response.text}
    




def convert_to_binary_image(image_path):
        with open(image_path, "rb") as f:
            png_encoded = f.read()
            print(png_encoded)
        return png_encoded
