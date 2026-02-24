from confluent_kafka import Producer
import json
import os


KAFKA_HOST = os.getenv("KAFKA_HOST", "kafka")
KAFKA_PORT = int(os.getenv("KAFKA_PORT", '9092'))

producer_config = {
    'bootstrap.servers':f"{KAFKA_HOST}:{KAFKA_PORT}",
    'acks':'all'}

class ProducerConn:
    producer = Producer(producer_config)

    @staticmethod
    def send_event_to_kafka(event):
        value = json.dumps(event)
        ProducerConn.producer.produce(
            topic="ROW",
            value=value,
        )
        ProducerConn.producer.poll(0)
        return
    
    @staticmethod
    def close_flush():
        ProducerConn.produce.flush()
        return