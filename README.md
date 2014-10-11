mqtt-client-python
==================

### NOTE: WIP (Work in Progress)

Example of connecting to ZADATA via MQTT using Python

``` bash
git clone git@github.com:zadata/mqtt-client-python.git
cd mqtt-client-python/

sudo pip install paho-mqtt
```

To find your MQTT Username and Password
login into your `ZADATA` account on http://ZADATA.com and click navbar -> `Settings` -> `Credentials`

NOTE: you have two MQTT passwords (one for subscribers only, the other with subscriber and publisher priveleges - use the one for publishers).

``` bash
export MQTT_USER=...
export MQTT_PWD=...
python mqtt_client.py
```
