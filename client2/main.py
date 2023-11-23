import datetime
import json
import os
import random
from time import sleep

import paho.mqtt.client as mqtt
import certifi


# The callback for when the client receives a CONNACK response from the server.
from dotenv import load_dotenv


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
# client.tls_set(certifi.where())
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.username_pw_set("juhani", "salasana")

# THIS TOKEN IS FROM RESTAPI'S /api/v1/token
load_dotenv()
TOKEN = os.getenv('TOKEN')
SENSORS = ['bathroom', 'bedroom', 'living room']
MIN = 17
MAX = 35

while True:

    temps = []

    for i in range(100):
        temp = random.randint(MIN, MAX)
        sensor_index = random.randint(0, len(SENSORS) - 1)
        _time = str(datetime.datetime.now())

        sensor_data = {'ts': _time, 'sensor': SENSORS[sensor_index], 'value': temp}
        temps.append(sensor_data)

    payload = json.dumps({'input': temps, 'token': TOKEN})
    client.publish("windows/node1/", payload)

    s = random.randint(1, 11)

    sleep(s)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
