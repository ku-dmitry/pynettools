#!/usr/bin/env python
import requests
import argparse
import re
import urllib.parse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target domain")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Target not specified. Use --help for more info.")
    return options


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))


def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urllib.parse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


input_options = get_arguments()
target_url = input_options.target
target_links = []
crawl(target_url)
print("[+] Job's done!")
