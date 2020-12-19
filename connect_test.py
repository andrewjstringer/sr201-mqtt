#!/usr/bin/env python3
# This is the Subscriber

import socket
# import sys


# Valid commands:
# 00 Obtain relay status, toggles nothing.
# 11 Turn relay 1 on
# 21 Turn relay 1 off
# 12 Turn relay 2 on
# 22 Turn relay 2 off

# Status output and command return values.
# 00000000 All relays off
# 01000000 2nd relay on
# 10000000 1st relay on
# 11000000 All relays on

def netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    #while True:
    #    data = s.recv(1024)
    #    if not data:
    #        break
    #    print("Inside func while", repr(data))
    #s.close()
    data = None
    while not data:
      data = s.recv(1024)
    s.close()
    print(repr(data))

    print("Inside func", repr(data))
    return repr(data)


ipaddress = '192.168.1.91'
device_port = 6722
command = '22:'

response = netcat(ipaddress, device_port, command)
print("Response >",response,"<")
