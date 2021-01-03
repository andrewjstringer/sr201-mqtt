#!/usr/bin/env python

import time
import paho.mqtt.client as paho
import socket
import sys

# MQTT parameters
broker = "krypton.int.rainsbrook.co.uk"
subscribe_topic = '/1stfloor/lights/relay1'
publish_topic = '/1stfloor/lights/relay1-status'
# brokerqos = 0


# sr201 parameters
sr201_ipaddress = '192.168.1.91'
sr201_port = 6722


def netcat(host, port, content):
    # talk to sr201
    print("sr201-netcat")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)

    data = None
    while not data:
        data = s.recv(1024)
    s.close()
    return repr(data)


def on_message(on_msg_client, userdata, message):
    time.sleep(1)
    rcvmsg = str(message.payload.decode("utf-8"))
    print('RcvdMsg', rcvmsg)

    if rcvmsg == 'On':
        print('On')
        command = '11:'
        print(command)
        response = netcat(sr201_ipaddress, sr201_port, command)
        allrelaystatus = [response[i:i+1] for i in range(0, len(response), 1)]
        print(allrelaystatus)
        relay1status = allrelaystatus[2]
        print("relay1status", relay1status)
        print(publish_topic)
        publishtomqtt(publish_topic, 'On', 0)
    elif rcvmsg == 'Off':
        print('Off')
        command = '21:'
        response = netcat(sr201_ipaddress, sr201_port, command)
        allrelaystatus = [response[i:i+1] for i in range(0, len(response), 1)]
        # print(allrelaystatus)
        relay1status = allrelaystatus[2]
        print("relay1status", relay1status)
        publishtomqtt(publish_topic, 'Off', 0)
    else:
        print('Error')


#def publishtomqtt(pubtopic, payload, qos):
#    client.connect(broker)  # may already be connected
#    client.publish(pubtopic, payload, qos)


# create client object client1.on_publish = on_publish
# assign function to callback client1.connect(broker,port)
# establish connection client1.publish("house/bulb1","on")
client = paho.Client("client-001")

print("connecting to broker ", broker)
client.connect(broker)  # connect
#client.on_message = on_message

print("subscribing to ", subscribe_topic)
# client.subscribe(subscribe_topic, qos=brokerqos)  # subscribe
client.subscribe(subscribe_topic)  # subscribe



# test
# publishtomqtt(publish_topic, 'Hello to you', 0)

while True:
    # ##### Bind function to callback
    client.on_message = on_message
    #####
    print("connecting to broker ", broker)
    client.connect(broker)  # connect
    client.loop_start()  # start loop to process received messages
    print("subscribing to ", subscribe_topic)
    print('.')
    time.sleep(2)
