import pyshark

# Define a function to extract fields as a dictionary
def extract_fields(packet):
    field_dict = {}
    for layer in packet.layers:
        layer_name = layer.layer_name
        field_dict[layer_name] = {}
        for field in layer.field_names:
            field_dict[layer_name][field] = getattr(layer, field, None)
    return field_dict

# Start live capture and filter specific fields (e.g., only TCP packets)
capture = pyshark.LiveCapture(interface='wlp1s0', display_filter='tcp')

# Process packets
for packet in capture.sniff_continuously(packet_count=1):  # Adjust count or use infinite loop
    fields = extract_fields(packet)
    import json
    with open('inspect pyshark.json','w') as file:
        json.dump(fields,file)
    print(fields)  # Print fields as a dictionary