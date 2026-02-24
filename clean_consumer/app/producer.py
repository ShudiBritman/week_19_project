from confluent_kafka import Producer
import logging
import json
import os


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

kafka_host = os.getenv("KAFKA_HOST", "localhost")
kafka_port = int(os.getenv("KAFKA_PORT", 9092))
bootstrap_servers = f"{kafka_host}:{kafka_port}"

producer_config = {
    'bootstrap.servers':bootstrap_servers,
    'acks':'all'}


producer = Producer(producer_config)
logger = logging.getLogger(__name__)

def delivery_report(err, msg):
    if err:
        logger.error("Delivery failed: %s", err)
    else:
        logger.info(
            "Delivered message: %s",
            msg.value().decode("utf-8")
        )
        logger.info(
            "Delivered to %s | partition %s | offset %s",
            msg.topic(),
            msg.partition(),
            msg.offset()
        )



def send_event_to_kafka(event):
        value = json.dumps(event)
        producer.produce(
            topic='CLEAN',
            value=value,
            callback=delivery_report
        )
        logger.info("seeding from file in batches of 10 every 5 seconds")
        producer.poll(0)


        producer.flush()
        return 