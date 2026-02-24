from pathlib import Path
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class Watcher:


    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    IMAGE_DIR = BASE_DIR / "tweet_images"

    VALID_EXTENSIONS = {".png"}

    @staticmethod
    def watch_dir():
        files = []

        for file_path in Watcher.IMAGE_DIR.iterdir():

            if not file_path.is_file():
                continue

            if file_path.name.startswith("."):
                continue

            if file_path.suffix.lower() not in Watcher.VALID_EXTENSIONS:
                continue

            files.append(str(file_path))
            
        return files


