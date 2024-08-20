# config.py
import os

COAP_SERVER_IP = os.environ['COAP_URL']
COAP_PORT = 5683
TEMPERATURE_URI = 'temperature'
HUMIDITY_URI = 'humidity'

# AWS IoT Core credentials and endpoint
NODE_ID = '1'
IOT_ENDPOINT = 'n91a830e.ala.eu-central-1.emqxsl.com'
CLIENT_ID = f'WeatherSensorNode{NODE_ID}'
PATH_TO_CERT = 'certs/weather.cert.pem'
PATH_TO_KEY = 'certs/weather.private.key'
PATH_TO_ROOT_CA = 'certs/root-CA.crt'  
SENSOR_DATA_TOPIC = 'sensor/data'
