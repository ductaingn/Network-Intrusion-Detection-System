import pyshark as ps
import json


class PysharkLiveCapture(object):
    def __init__(self, interface, send_every, send_format):
        self.interface = interface
        self.send_every = send_every
        self.send_format = send_format
        self.livecapture: ps.LiveCapture = ps.LiveCapture(interface)

    def format_packet(self, packet):
        if self.send_format == 'str':
            return str(packet)
        if self.send_format == 'json':
            return json.dumps({
                'length': packet.length,
            })
