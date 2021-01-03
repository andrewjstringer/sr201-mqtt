#!/usr/bin/env python

import time
import paho.mqtt.client as paho
import socket
import sys

broker = "krypton.int.rainsbrook.co.uk"

topic = '/1stfloor/lights/relay1'
ipaddress = '192.168.1.91'
device_port = 6722
brokerqos = 0


def netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)

    data = None
    while not data:
        data = s.recv(1024)
    s.close()
    # print(repr(data))
    # print("Inside func", repr(data))
    return repr(data)


def on_message(client, userdata, message):
    time.sleep(1)
    rcvmsg = str(message.payload.decode("utf-8"))
    # print('RcvdMsg', rcvmsg)

    if rcvmsg == 'On':
        print('On')
        command = '11:'
        response = netcat(ipaddress, device_port, command)
        # print("Response >", response, "<")
        allrelaystatus = [response[i:i+1] for i in range(0, len(response), 1)]
        # print(allrelaystatus)
        relay1status = allrelaystatus[2]
        print("relay1status", relay1status)
    elif rcvmsg == 'Off':
        print('Off')
        command = '21:'
        response = netcat(ipaddress, device_port, command)
        # print("Response >", response, "<")
        allrelaystatus = [response[i:i+1] for i in range(0, len(response), 1)]
        # print(allrelaystatus)
        relay1status = allrelaystatus[2]
        print("relay1status", relay1status)
    else:
        print('Error')


# create client object client1.on_publish = on_publish
# assign function to callback client1.connect(broker,port)
# establish connection client1.publish("house/bulb1","on")
client = paho.Client("client-001")

print("connecting to broker ", broker)
client.connect(broker)  # connect
client.on_message = on_message

print("subscribing to ", topic)
client.subscribe(topic, qos=brokerqos)  # subscribe

while True:
    # ##### Bind function to callback
    # client.on_message = on_message
    #####
    # print("connecting to broker ", broker)
    # client.connect(broker)  # connect
    client.loop_start()  # start loop to process received messages
    # print("subscribing to ", topic)
    # client.subscribe(topic,qos = brokerqos)  # subscribe
    time.sleep(2)
