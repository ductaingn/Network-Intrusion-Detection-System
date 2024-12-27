import json

from pyshark.packet.packet import Packet as PysharkPacket
from scapy.packet import Packet as ScapyPacket
from scapy.layers.inet import *
from cicflowmeter.flow_session import FlowSession

# FlowSession requires 'output_mode' and 'output' to be set so it cans initiate output_writer
# We are using a custom output_writer but still need to declare these fields for FlowSession to initiate,
setattr(FlowSession, 'output_mode', 'url')
setattr(FlowSession, 'output', 'placeholder')


def pyshark2scapy(pyshark_packet: PysharkPacket) -> ScapyPacket:
    """
    Converts a pyshark Packet into a scapy Packet
    """

    first_layer_name = pyshark_packet.layers[0].layer_name

    if first_layer_name == 'eth':
        return Ether(pyshark_packet.get_raw_packet())
    if first_layer_name == 'sll':
        return CookedLinux(pyshark_packet.get_raw_packet())

    raise NotImplementedError(f'Unsupported first layer type: {first_layer_name}')


class ListWriter:
    """
    Custom writer for cicflowmeter FlowSession, writes data into a dict that is convertable to pd.DataFrame
    """

    def __init__(self, output: list[dict]):
        self.output = output

    def write(self, data: dict):
        self.output.append(data)


class PacketAnalyzer:
    """
    Analyzes pyshark packets into a json string that when converted to a dict can be converted into a DataFrame
    """

    def __init__(self):
        self.data = []
        self.session = FlowSession()
        self.session.output_writer = ListWriter(self.data)

    def add_packet(self, packet: PysharkPacket):
        self.session.on_packet_received(pyshark2scapy(packet))

    def collect_results(self) -> list[dict]:
        self.session.toPacketList()

        result = self.data.copy()
        self.data.clear()
        self.session = FlowSession()
        self.session.output_writer = ListWriter(self.data)

        return result
