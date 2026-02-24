import logging
import os
import json
from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient, NewTopic
from clean import clean_and_upper_case_text
from producer import send_event_to_kafka


logger = logging.getLogger(__name__)

kafka_host = os.getenv("KAFKA_HOST", "localhost")
kafka_port = int(os.getenv("KAFKA_PORT", 9092))
bootstrap_servers = f"{kafka_host}:{kafka_port}"
#TOPIC_NAME = os.getenv("TOPIC_NAME", "users-orders.registered")


class ConsumerConn:

    @staticmethod
    def ensure_topic_exists():
        admin = AdminClient({f'bootstrap.servers':bootstrap_servers})
        topic = NewTopic(
            topic='ROW',
            num_partitions=1,
            replication_factor=1
        )
        admin.create_topics([topic])

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
            clean_image_text = clean_and_upper_case_text(image_details['image_text'])
            image_details['image_text'] = clean_image_text
            
            send_event_to_kafka(image_details)
            
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def consume_loop():
        consumer = ConsumerConn.create_consumer()
        ConsumerConn.ensure_topic_exists()

        consumer.subscribe(['ROW'])
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