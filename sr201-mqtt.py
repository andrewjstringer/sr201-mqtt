#!/usr/bin/env python

import time
import paho.mqtt.client as paho
import socket
import config
from datetime import datetime


# This function connects to the sr-201 device, host and port are defined in the
# config.py file, the content is served from the relay number and action requested.
def netcat(host, port, content):
    nc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nc_socket.connect((host, int(port)))
    nc_socket.sendall(content.encode())
    nc_socket.shutdown(socket.SHUT_WR)

    data = None
    while not data:
        data = nc_socket.recv(1024)
    nc_socket.close()
    # print(repr(data))
    return repr(data)


def on_message(client, userdata, message):
    time.sleep(1)
    rcvmsg = str(message.payload.decode("utf-8"))
    # print('RcvdMsg', rcvmsg)
    now = datetime.now()
    nowstr = now.strftime("%d/%m/%Y, %H:%M:%S")
    statusbase = 1

    # code listens to mqtt topic, allowed values are 'On', 'Off' and 'Status'
    if rcvmsg == "On":
        print(nowstr, " On")
        command = "1" + config.relaynumber + ":"
        response = netcat(config.ipaddress, config.device_port, command)
        allrelaystatus = [response[i:i+1] for i in range(0, len(response), 1)]
        # print(allrelaystatus)
        statusindex = statusbase + int(config.relaynumber)
        # print("statusindex is", statusindex)
        relaystatus = allrelaystatus[statusindex]
        # Write status back to mqtt
        publishtomqtt(config.publish_topic, relaystatus, 0)
    elif rcvmsg == "Off":
        print(nowstr, ' Off')
        command = "2" + config.relaynumber + ":"
        response = netcat(config.ipaddress, config.device_port, command)
        allrelaystatus = [response[i:i+1] for i in range(0, len(response), 1)]
        # print(allrelaystatus)
        statusindex = statusbase + int(config.relaynumber)
        # print("statusindex is", statusindex)
        relaystatus = allrelaystatus[statusindex]
        publishtomqtt(config.publish_topic, relaystatus, 0)
    elif rcvmsg =="Status":
        print(nowstr, " Status")
        command = "00" + ":"
        response = netcat(config.ipaddress, config.device_port, command)
        allrelaystatus = [response[i:i + 1] for i in range(0, len(response), 1)]
        # print("allrelaystatus is:- ", allrelaystatus)
        statusindex = statusbase + int(config.relaynumber)
        # print("statusindex is", statusindex)
        relaystatus = allrelaystatus[statusindex]
        # print("relaystatus", relaystatus)
        publishtomqtt(config.publish_topic, relaystatus, 0)
    else:
        print("Error")


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
