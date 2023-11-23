import json
import os
from ast import literal_eval

import jwt
import paho.mqtt.client as mqtt
import certifi
import requests
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

USE_API = True

load_dotenv()
# MAKE SURE YOUR MONGODB_URL IS IN .env
uri = os.getenv('MONGODB_URL')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    db = client.iotexample
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# MAKE SURE YOUR cert DIR IS PRESENT


class AsymmetricToken:
    def __init__(self):
        with open('cert/id_rsa.pub') as f:
            self.public = f.read()

    def validate(self, t):
        claims = jwt.decode(t, self.public, algorithms=['RS512'], audience='iot')
        return claims


_token = AsymmetricToken()

# SENDS SENSOR DATA TO API
def insert_using_api(data):
    # MAKE SURE YOUR RESTAPI_URL is IN .env
    requests.post(os.getenv('RESTAPI_URL'), json=data['input'],
                  headers={'Authorization': f'Bearer {data["token"]}'})

# INSERTS DATA STRAIGHT INTO DB
def insert_in_mqtt(data):

    # only users haveing iot role, can insert data

    decoded = _token.validate(data['token'])
    user = db.users.find_one({'_id': ObjectId(decoded['sub'])})
    if user['role'] == 'iot':
        db.sensor_data.insert_many(data['input'])


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("windows/node1/")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        data = literal_eval(msg.payload.decode('utf8'))
        if not USE_API:
            insert_in_mqtt(data)
        else:
            insert_using_api(data)
    except Exception as _e:
        print(_e)


client = mqtt.Client()
# CHANGE THESE CREDENTIALS TO FIT YOUR REQUIREMENTS
client.username_pw_set("juhani", "salasana")

# client.tls_set(certifi.where())
client.on_connect = on_connect
client.on_message = on_message

# IF YOU DON'T HAVE LOCAL BROKER, CHANGE THIS TO FIT YOUR REQUIREMENTS
client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
