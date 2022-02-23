#!/usr/bin/env python
import scanner
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target domain")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Target not specified. Use --help for more info.")
    return options


input_options = get_arguments()
target_url = input_options.target
links_to_ignore = ["logout.php"]

data_dict = {"username": "admin", "password": "password", "login": "submit"}

vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
vuln_scanner.session.post(target_url, data=data_dict)

vuln_scanner.crawl()
vuln_scanner.run_scanner()
