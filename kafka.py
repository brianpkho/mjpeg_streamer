from confluent_kafka import Consumer, Producer
import json
import socket


class Kafka:
    def __init__(self):
        self.credentials = {
            'bootstrap.servers': 'localhost:9092',
            'client.id': socket.gethostname()
        }

        self.producer = self.connect(self.credentials)
        self.message_key = "Helo world"
        self.topics = 'test'

    def connect(self, credentials):
        try:
            producer = Producer(**self.credentials)
            print("connected to kafka")

            return producer
        except Exception as e:
            print("error connecting to kafka: %s" % str(repr(e)))
    
    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
    
    def send_kafka_message(self, message_value, topic):
        self.producer.produce(
            topic,
            value=message_value,
            key=self.message_key.encode(),
            callback=self.delivery_report
        )
        self.producer.flush()