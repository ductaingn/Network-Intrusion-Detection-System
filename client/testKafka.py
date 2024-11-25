import pyshark
from kafka import KafkaProducer

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Replace with your Kafka broker address
    value_serializer=lambda v: v.encode('utf-8')  # Serialize packet data as UTF-8
)

# Function to send packet to Kafka
def send_packet_to_kafka(packet):
    try:
        # Convert packet to a string or JSON if needed
        packet_data = str(packet)

        # Send to Kafka topic
        producer.send('quickstart-events', value=packet_data)
        print(f"Sent packet to Kafka: {packet_data}")
    except Exception as e:
        print(f"Error sending packet: {e}")

# Start capturing packets using pyshark

print("Capturing packets and sending to Kafka...")
capture = pyshark.LiveCapture(interface='wlp1s0')  # Replace 'eth0' with your network interface

while True:
    for packet in capture.sniff_continuously(5):
        send_packet_to_kafka(packet)