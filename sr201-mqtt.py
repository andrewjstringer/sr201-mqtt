#!/usr/bin/env python

import time
import paho.mqtt.client as paho
import socket
import config
from datetime import datetime


# This function connects to the sr-201 device, host and port are defined in the
# config.py file, the contect is serived from the relay number and action requested.
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
    return repr(data)


def on_message(client, userdata, message):
    time.sleep(1)
    rcvmsg = str(message.payload.decode("utf-8"))
    # print('RcvdMsg', rcvmsg)
    now = datetime.now()
    nowstring = now.strftime("%d/%m/%Y, %H:%M:%S")
    statusbase = 1

    if rcvmsg == 'On':
        print(nowstring, ' On')
        command = '1' + config.relaynumber + ':'
        response = netcat(config.ipaddress, config.device_port, command)
        allrelaystatus = [response[i:i+1] for i in range(0, len(response), 1)]
        # print(allrelaystatus)
        statusindex = statusbase + int(config.relaynumber)
        # print('statusindex is', statusindex)
        relaystatus = allrelaystatus[statusindex]
        publishtomqtt(config.publish_topic, relaystatus, 0)
    elif rcvmsg == 'Off':
        print(nowstring, ' Off')
        command = '2' + config.relaynumber + ':'
        response = netcat(config.ipaddress, config.device_port, command)
        allrelaystatus = [response[i:i+1] for i in range(0, len(response), 1)]
        # print(allrelaystatus)
        statusindex = statusbase + int(config.relaynumber)
        # print('statusindex is', statusindex)
        relaystatus = allrelaystatus[statusindex]
        publishtomqtt(config.publish_topic, relaystatus, 0)
    elif rcvmsg =='Status':
        print(nowstring, ' Status')
        command = '00' + ':'
        response = netcat(config.ipaddress, config.device_port, command)
        allrelaystatus = [response[i:i + 1] for i in range(0, len(response), 1)]
        # print('allrelaystatus is:- ', allrelaystatus)
        statusindex = statusbase + int(config.relaynumber)
        # print('statusindex is', statusindex)
        relaystatus = allrelaystatus[statusindex]
        # print("relaystatus", relaystatus)
        publishtomqtt(config.publish_topic, relaystatus, 0)

    else:
        print('Error')


def publishtomqtt(pubtopic, payload, qos):
    # clientpub.connect(broker)  # may already be connected
    # print("From in publishtomqtt", pubtopic, payload, qos)
    clientpub.publish(pubtopic, payload, qos)


clientsub = paho.Client("clientsub-001")
clientpub = paho.Client("clientsub-002")

print("connecting to broker ", config.broker)
clientsub.connect(config.broker)  # connect
clientsub.on_message = on_message

clientpub.connect(config.broker)  # may already be connected

print("subscribing to ", config.subscribe_topic)
clientsub.subscribe(config.subscribe_topic, qos=config.brokerqos)  # subscribe

print("publishing to ", config.publish_topic)

while True:
    # Also test loop_forever()
    clientsub.loop_start()  # start loop to process received messages
    # print("subscribing to ", subscribe_topic)
    # clientsub.subscribe(config.subscribe_topic,qos = config.brokerqos)  # subscribe
    time.sleep(2)
