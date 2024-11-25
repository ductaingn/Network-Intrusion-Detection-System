from kafka import KafkaProducer

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='192.168.143.20:9092',  # Replace with your Kafka broker address
    value_serializer=lambda v: v.encode('utf-8')  # Serialize packet data as UTF-8
)
producer.send('test', value='hello world!')
