#!/usr/bin/env python
import requests
import requests.exceptions
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target domain")
    parser.add_argument("-s", "--subdomains", action='store_true', help="Check subdomains")
    parser.add_argument("-d", "--dirs", action="store_true", help="Check common sub-dirs")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Target not specified. Use --help for more info.")
    return options


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


input_options = get_arguments()

target_url = input_options.target
if input_options.subdomains:
    with open("subdomain.list", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = word + "." + target_url
            response = request(test_url)
            if response:
                print("[+] Discovered subdomain: " + test_url)
if input_options.dirs:
    with open("dir.list", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = target_url + "/" + word
            response = request(test_url)
            if response:
                print("[+] Discovered subdomain: " + test_url)
print("All done, exiting. If there was no input make sure you added -s or -d flag.")
