import logging
import os
import json
from confluent_kafka import Consumer
from dal import *
from utils import build_index_schema

logger = logging.getLogger(__name__)

kafka_host = os.getenv("KAFKA_HOST", "localhost")
kafka_port = int(os.getenv("KAFKA_PORT", 9092))
bootstrap_servers = f"{kafka_host}:{kafka_port}"


class ConsumerConn:

    @staticmethod
    def create_consumer():
        config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': 'clean-consumer',
            'auto.offset.reset': 'earliest'
        }
        return Consumer(config)


    @staticmethod
    def handle_message(msg):
        value = msg.value().decode('utf-8')
        try:
            image_details = json.loads(value)
            schema_to_index = build_index_schema(image_details, "clean_upper")
            image_id = schema_to_index['id']
            create_index()
            update_doc(schema_to_index, image_id)
            
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def consumer_loop():
        consumer = ConsumerConn.create_consumer()

        consumer.subscribe(['CLEAN'])
        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue

                if msg.error():
                    logger.error(msg.error())
                    continue

                ConsumerConn.handle_message(msg)

        finally:
            consumer.close()