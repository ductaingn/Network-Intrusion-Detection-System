import json
from model.Pyshark import PysharkLiveCapture
from model.Producer import Producer
from pyshark import LiveCapture
from kafka import KafkaProducer


def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)


if __name__ == '__main__':
    config = load_config('configs.json')

    # Extract Kafka configuration
    kafka_config = config["kafka"]
    pyshark_config = config["pyshark"]

    # producer = KafkaProducer(
    #     bootstrap_servers=kafka_config['bootstrap_servers'],
    #     value_serializer=lambda v: v.encode(
    #         'utf-8'),
    #     key_serializer=lambda k: k.encode('utf-8')  # Serialize key as UTF-8
    # )

    producer = Producer(kafka_config)

    pysharkLivecapture = PysharkLiveCapture(
        interface=pyshark_config['interface'],
        send_every=pyshark_config['send_every'],
        send_format=pyshark_config['send_format'])

    for i, packet in enumerate(pysharkLivecapture.livecapture.sniff_continuously(packet_count=pysharkLivecapture.send_every)):
        try:
            # Convert the packet into a JSON string
            packet = pysharkLivecapture.format_packet(packet)

            # Send the data
            producer.send_data(key=f'testing_key_{i}', value=packet)
            print(f"Packet {i} sent successfully.")
        except Exception as e:
            print(f"Error sending packet {i}: {e}")

    producer.kafka_producer.flush()  # Ensure all messages are sent before exiting
