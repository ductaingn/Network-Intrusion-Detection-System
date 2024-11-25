from kafka import KafkaProducer

class Producer:
    def __init__(self, **config):
        self.producer = KafkaProducer(config)
        pass