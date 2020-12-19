#!/usr/bin/env python

import time
import paho.mqtt.client as paho
broker="krypton.int.rainsbrook.co.uk"
# broker="iot.eclipse.org"
# define callback


def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =", str(message.payload.decode("utf-8")))


# create client object client1.on_publish = on_publish
# assign function to callback client1.connect(broker,port)
# establish connection client1.publish("house/bulb1","on")
client= paho.Client("client-001")


# ##### Bind function to callback
client.on_message=on_message
#####
print("connecting to broker ",broker)
client.connect(broker) # connect
client.loop_start() # start loop to process received messages
print("subscribing ")
client.subscribe("topic/test1")  # subscribe
time.sleep(2)

print("publishing ")
client.publish("topic/test1", "off")  # publish
time.sleep(4)
client.disconnect()  # disconnect
client.loop_stop()  # stop loop

