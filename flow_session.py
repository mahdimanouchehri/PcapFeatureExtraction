from scapy.all import rdpcap
from scapy.sendrecv import sniff
from features.context.packet_direction import PacketDirection
from features.context.packet_flow_key import get_packet_flow_key
from flow import Flow
from tqdm import tqdm

EXPIRED_UPDATE = 40
class FlowSession:

    """Creates a list of network flows."""
    def __init__(self, pcap_link):

        self.pcap_link = pcap_link
        self.packets = self.read_pcap()
        self.packets_count = 0
        self.flows = {}

    def create_flows(self):
        for packet in tqdm(self.packets):
            self.on_packet_received(packet)

    def read_pcap(self):
        #packets = sniff(offline=self.pcap_link)
        packets = rdpcap(self.pcap_link) # alternative way for read pcap file
        return packets

    def get_flows(self) -> list:
        return self.flows.values()

    def on_packet_received(self, packet):
        count = 0
        direction = PacketDirection.FORWARD

        # if "TCP" not in packet:
        #     return
        #
        # elif "UDP" not in packet:
        #     return

        try:
            # Creates a key variable to check
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))
        except Exception:
            return

        self.packets_count += 1

        # If there is no forward flow with a count of 0
        if flow is None:
            # There might be one of it in reverse
            direction = PacketDirection.REVERSE
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))

        if flow is None:
            # If no flow exists create a new flow
            direction = PacketDirection.FORWARD
            flow = Flow(packet, direction)
            packet_flow_key = get_packet_flow_key(packet, direction)
            self.flows[(packet_flow_key, count)] = flow

        elif (packet.time - flow.latest_timestamp) > EXPIRED_UPDATE:
            # If the packet exists in the flow but the packet is sent
            # after too much of a delay than it is a part of a new flow.
            expired = EXPIRED_UPDATE
            while (packet.time - flow.latest_timestamp) > expired:
                count += 1
                expired += EXPIRED_UPDATE
                flow = self.flows.get((packet_flow_key, count))

                if flow is None:
                    flow = Flow(packet, direction)
                    self.flows[(packet_flow_key, count)] = flow
                    break

        elif "F" in str(packet.flags):
            # If it has FIN flag then early collect flow and continue
            flow.add_packet(packet, direction)
            #self.garbage_collect(packet.time)
            return

        flow.add_packet(packet, direction)
    #    print("flow:", flow)


