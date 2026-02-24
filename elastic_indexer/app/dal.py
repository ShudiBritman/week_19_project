from elastic_connection import get_connection
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger(__name__)


es = get_connection()


def create_index():
    mapping = {
    "mappings": {
        "dynamic": True,
        "properties": {
        "id": {
            "type": "keyword"
        },
        "meta_data": {
            "type": "object",
            "properties": {
            "file_size": {
                "type": "long"
            },
            "width": {
                "type": "integer"
            },
            "height": {
                "type": "integer"
            },
            "format_file": {
                "type": "keyword"
            }
            }
        },
        "image_text": {
            "type": "object",
            "properties": {
            "raw": {
                "type": "text"
            },
            "clean_upper": {
                "type": "text"
            },
            "analytics": {
                "type": "text"
            }
            }
        }
        }
    }
    }
    if not es.indices.exists(index="images"):
        es.indices.create(index="images", body=mapping)
        logger.info("created index")
        return
    else:
        logger.info("index exists")
        return


def update_doc(data, image_id):
    es.update(
    index="images",
    id=image_id,
    doc=data,
    doc_as_upsert=True
)
    logger.debug("index updated %s", image_id)