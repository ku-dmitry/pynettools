#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Interface not specified. Use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] New MAC not specified. Use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("Could not read MAC address!")


input_options = get_arguments()

current_mac = get_current_mac(input_options.interface)
print("Current MAC = " + str(current_mac))

change_mac(input_options.interface, input_options.new_mac)

current_mac = get_current_mac(input_options.interface)
if current_mac == input_options.new_mac:
    print("[+] MAC address has been successfully changed!")
else:
    print("[-] Something went wrong! MAC was not changed!")
