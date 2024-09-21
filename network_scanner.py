from sre_parse import Verbose
from tabnanny import verbose
import  argparse
import scapy.all as scapy

def get_arguments():
    parser = argparse.ArgumentParser(description='ARP')
    parser.add_argument("--t", "--target", dest="target", help="IP range to scann")
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Please specify an IP range use --help for more info.")
    return args

def scan(ip):
    arp_request = scapy.ARP(pdst = ip) #Who has this ip? using an ARP request
    #arp_request.show() Show details of the packet
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") #Ethernet object
    arp_request_broadcast = broadcast/arp_request #New packet
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]#Function send and recieve customized
    # print(answered_list.summary())
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

args = get_arguments()
#print(args.target)
scan_result = scan(str(args.target))
print_result(scan_result)