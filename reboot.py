#! /usr/bin/python3

import os
import socket
UDP_IP = "10.39.54.191"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message: %s" % data)
        if data.decode("ascii") == "REBOOT":
                os.system('reboot -f')
                print("rebooting...")
