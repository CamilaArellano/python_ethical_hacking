import subprocess
import argparse
import re

def get_arguments():
    parser = argparse.ArgumentParser(description='Mac changer')
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New Mac address")
    args = parser.parse_args()
    if not args.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not args.new_mac:
        parser.error("[-] Please specify an MAC, use --help for more info.")
    return args

def change_mac(interface, new_mac):
    print("Changing MAC address for " + interface + " to " + new_mac)

    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result_str = ifconfig_result.decode('utf-8')  # Decodificar los bytes a una cadena de texto
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result_str)
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("Could not read MAC address")


args = get_arguments()

current_mac = get_current_mac(args.interface)
print("Current MAC = " + str(current_mac))

change_mac(args.interface, args.new_mac)

current_mac = get_current_mac(args.interface)
if current_mac == args.new_mac:
    print("MAC address was successfully changed to " + str(current_mac))
else:
    print("MAC address did not get changed")

