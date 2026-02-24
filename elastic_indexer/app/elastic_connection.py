from elasticsearch import Elasticsearch
import logging
import time
import os


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

elastic_host = os.getenv("ELASTIC_HOST")
elastic_port = os.getenv("ELASTIC_PORT")


def get_connection():
    for i in range(30):
        try:
            uri = f"http://{elastic_host}:{elastic_port}"
            es = Elasticsearch(uri)
            if es.ping():
                logger.info("Connected to Elasticsearch")
                return es
        except Exception:
            pass

        logger.warning("Waiting for Elasticsearch...")
        time.sleep(2)

    raise Exception("Failed to connect")




