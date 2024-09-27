import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    # Verificar si es un paquete HTTP Request en IPv4 o IPv6
    if packet.haslayer(http.HTTPRequest):  # Solo HTTP en IPv4
        url = packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode()
        print(f"[*] HTTP Request to: {url}")
        info = get_info(packet)
        if info:
            print(f"\n[*] Payload: {info}\n")  # Quitar el 'print' adicional

def get_info(packet):
    if packet.haslayer(scapy.Raw):  # Verificar si hay un payload en el paquete (datos POST)
        load = packet[scapy.Raw].load.decode(errors="ignore")
        return load

sniff("wlo1")
