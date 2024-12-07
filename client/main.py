import json
from client.model.PacketAnalyzer import PacketAnalyzer
from model.Pyshark import PysharkLiveCapture
from model.Producer import Producer


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

    analyzer = PacketAnalyzer()

    for i, packet in enumerate(pysharkLivecapture.livecapture.sniff_continuously()):
        try:
            analyzer.add_packet(packet)
            print(f"Received packet {i}.")

            if i > 0 and i % pysharkLivecapture.send_every == 0:
                result = analyzer.collect_result()
                producer.send_data(key=f'testing_key_{i}', value=result)

                print(f"Analyzed packets collected and sent successfully.")
                print(result)
                break
        except Exception as e:
            print(f"Error sending at packet {i}: {e}")

    producer.kafka_producer.flush()  # Ensure all messages are sent before exiting
