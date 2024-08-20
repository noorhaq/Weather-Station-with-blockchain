import asyncio
import paho.mqtt.client as mqtt
import config
import json
import logging
import ssl

logging.basicConfig(level=logging.DEBUG)

# Initialize MQTT client
context = ssl.create_default_context()
context.load_verify_locations(cafile=config.MQTT_CA_CERT)
# context.load_cert_chain(certfile=config.MQTT_CERT, keyfile=config.MQTT_PRIVATE_KEY)

mqtt_client = mqtt.Client()
mqtt_client.tls_set_context(context)

temperature = 25.5  # Global values
humidity = 30.0

def fetch_temperature():
    return temperature 

def fetch_humidity():
    return humidity

def on_connect(client, userdata, flags, rc, *args):
    if rc == 0:
        print(f"MQTT connected with result code {rc}")
        client.subscribe(config.MQTT_TOPIC)
    else:
        print(f"MQTT connection failed with result code {rc}")
        print("Retrying connection in 5 seconds...")
        client.reconnect_delay_set(5)  # Set reconnection delay to 5 seconds

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"Received MQTT data on topic {msg.topic}:")
        print(data)

        global temperature, humidity
        if 'temperature' in data:
            temperature = data['temperature']
            print(f"Temperature: {temperature}")
        if 'humidity' in data:
            humidity = data['humidity']
            print(f"Humidity: {humidity}")
        else:
            print("Invalid data format")
    except json.JSONDecodeError:
        print("Invalid JSON data")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

async def start_mqtt_client():
    try:
        mqtt_client.username_pw_set(username='noor', password='noor1234')
        mqtt_client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
        mqtt_client.loop_start()  # Start the loop in a separate thread
        while True:
            await asyncio.sleep(1)  # Keep the loop running
    except ConnectionRefusedError:
        print("Connection refused. Check MQTT broker and port.")
    except Exception as e:
        print(f"An error occurred: {e}")
