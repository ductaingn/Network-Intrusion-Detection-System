import json
from model.PacketAnalyzer import PacketAnalyzer
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

    producer = Producer(kafka_config)

    pysharkLivecapture = PysharkLiveCapture(
        interface=pyshark_config['interface'],
        send_every=pyshark_config['send_every'],
        send_format=pyshark_config['send_format'])

    analyzer = PacketAnalyzer()

    while True:
        for i, packet in enumerate(pysharkLivecapture.livecapture.sniff_continuously(pysharkLivecapture.send_every)):
            analyzer.add_packet(packet)
            print(f"Received packet {i}.")

        try:
            result = analyzer.collect_result()
            if result == '{}':
                continue

            producer.send_data(key=f'testing_key_{i}', value=result)

            print(f"Analyzed packets collected and sent successfully.")
            print(result)
        except Exception as e:
            print(f"Error sending at packet {i}: {e}")

        break

    producer.kafka_producer.flush()  # Ensure all messages are sent before exiting
