from kafka import KafkaProducer
import json


class Producer(object):
    def __init__(self, configs):
        super().__init__()
        self.kafka_server = configs['bootstrap_servers']
        self.kafka_topic = configs['topic']
        self.kafka_producer: KafkaProducer = KafkaProducer(
            bootstrap_servers=self.kafka_server,
            value_serializer=lambda v: v.encode(
                'utf-8'),  # Serialize value as JSON
            key_serializer=lambda k: k.encode(
                'utf-8')  # Serialize key as UTF-8)
        )

    def send_data(self, key, value):
        '''
        Send data
        '''
        try:
            self.kafka_producer.send(
                topic=self.kafka_topic,
                value=value,
                key=key)
        except Exception as e:
            print(f"Error sending packet: {e}, key:{key}")
