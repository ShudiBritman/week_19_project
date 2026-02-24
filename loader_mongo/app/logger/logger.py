import logging
import os

LOG_DIR = "logs"
LOG_FILE = "service.log"

os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name="service_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:

        file_handler = logging.FileHandler(
            os.path.join(LOG_DIR, LOG_FILE),
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger