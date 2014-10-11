#! /usr/bin/python

# TODO: add subscription 
# TODO: better publish example

################################################################################
# Uses Paho MQTT Python client library.
# See: 
#   https://pypi.python.org/pypi/paho-mqtt
#   http://mosquitto.org/2013/12/paho-mqtt-python-client/
#   http://www.eclipse.org/paho/
#   http://git.eclipse.org/c/paho/org.eclipse.paho.mqtt.python.git/
#
# HOW TO RUN:
#   sudo pip install paho-mqtt
#   python mqtt_client.py
#
# Author: Zvi Avraham <zvi-AT-zadata-DOT-com>
# Copyright 2012-2014 ZADATA Ltd. All Rights Reserved.
################################################################################

import os
import time
import traceback
import threading

#import mosquitto # install libmosquitto python binding
import paho.mqtt.client as mqtt

# TODO : need to handle reconnects

# return default value if environment variable is not exist
def env(env_var, default_val):
    return default_val if env_var not in os.environ else os.environ[env_var]

# MQTT connection settings
MQTT_HOST = "mqtt.zadata.com"
MQTT_PORT = 1883
MQTT_USER = env('MQTT_USER', '')
MQTT_PWD  = env('MQTT_PWD', '')
MQTT_KEEPALIVE_SEC = 25

DEMO_DEBUG = int(env('DEMO_DEBUG', 0)) != 0

def log(msg):
    if DEMO_DEBUG:
        print msg

class MQTTClient:

    def __init__(self):
        client_id = "%s_%s" % (__file__, os.urandom(4).encode("hex"))
        log("client_id = %s" % client_id)

        self.shutdown = False
        #self.client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311)
                                                    # TODO - change protocol to mqtt.MQTTv311 later
        self.client = mqtt.Client(client_id=client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)

        self.client.username_pw_set(MQTT_USER, MQTT_PWD)
        self.client.on_connect = self.on_connect
        self.client.connect(MQTT_HOST, MQTT_PORT, keepalive=MQTT_KEEPALIVE_SEC)
        log("connect done")
        try:
            while True:
                self.client.loop(1000)
        except:
            self.client.disconnect()
            self.shutdown = True;

    # # CONNACK codes
    # CONNACK_ACCEPTED = 0
    # CONNACK_REFUSED_PROTOCOL_VERSION = 1
    # CONNACK_REFUSED_IDENTIFIER_REJECTED = 2
    # CONNACK_REFUSED_SERVER_UNAVAILABLE = 3
    # CONNACK_REFUSED_BAD_USERNAME_PASSWORD = 4
    # CONNACK_REFUSED_NOT_AUTHORIZED = 5

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        log("on_connect rc=%d" % rc)
        # TODO - handle cases rc!=0 - i.e. connect errors
        if rc == 0:
            self.publish_thread = threading.Thread(target=self.do_publish_thread)
            self.publish_thread.start()

    def do_publish_thread(self):
        log("do_publish_thread")
        self.publish_meta()
        self.latest_event = 0
        while True:
            log("publishing")
            try:
                self.publish("hello", "Hello World!")
            except:
                traceback.print_exc()
            log("Sleeping for a minute")
            time.sleep(60)

    def publish(self, topic, value):
        log("Publish to %s value %s" % (topic, value))
        self.client.publish(topic, value, retain=True)

def main():   
    client = MQTTClient()

if __name__ == '__main__':
    main()
