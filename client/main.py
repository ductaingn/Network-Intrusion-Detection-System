import json
from model.PacketAnalyzer import PacketAnalyzer
from model.Pyshark import PysharkLiveCapture
from model.Producer import Producer
import utilities as utils

if __name__ == '__main__':
    config = utils.load_config('configs.json')
    my_ip = utils.get_ip()

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
            result = analyzer.collect_results()
            if not result:
                continue

            for flow in result:
                producer.send_data(key=f'{my_ip}', value=json.dumps(flow))
                print('Sent', json.dumps(flow))

        except Exception as e:
            print(f"Error sending at packet {i}: {e}")

        producer.kafka_producer.flush()  # Ensure all messages are sent before exiting
        # break

