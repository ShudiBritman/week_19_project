import logging
import os
import json
from confluent_kafka import Consumer
from managment_flow import managment
logger = logging.getLogger(__name__)

kafka_host = os.getenv("KAFKA_HOST", "localhost")
kafka_port = int(os.getenv("KAFKA_PORT", 9092))
bootstrap_servers = f"{kafka_host}:{kafka_port}"


class ConsumerConn:

    @staticmethod
    def create_consumer():
        config = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': 'clean-service-tracker',
            'auto.offset.reset': 'earliest'
        }
        return Consumer(config)

    @staticmethod
    def handle_message(msg):
        value = msg.value().decode('utf-8')
        try:
            image_details = json.loads(value)
            image_id = image_details['id']
            image_text = image_details['image_text']
            managment(image_id, image_text)
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def consume_loop():
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