# config.py
import os

# CoAP Server Configuration
# COAP_SERVER_IP = 'coap://COAPServer:5683'
COAP_SERVER_IP = os.environ['COAP_URL']
COAP_PORT = 5683

# MQTT Configuration for AWS IoT Core
NODE_ID = '1'
MQTT_BROKER = 'n91a830e.ala.eu-central-1.emqxsl.com'
MQTT_PORT = 8883
MQTT_TOPIC = 'sensor/data'
MQTT_CLIENT_ID = f'WeatherSensorNode{NODE_ID}'
MQTT_CA_CERT = 'certs/root-CA.crt'
MQTT_CERT = 'certs/weather.cert.pem'
MQTT_PRIVATE_KEY = 'certs/weather.private.key'
