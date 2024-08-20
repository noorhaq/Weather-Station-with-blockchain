import json
import time
import paho.mqtt.client as mqtt
from weather_data import get_temperature, get_humidity
import config

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Callback when a message is published
def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")

# Create the MQTT client
mqtt_client = mqtt.Client(client_id=config.CLIENT_ID)
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish

# Configure the MQTT client with TLS
mqtt_client.tls_set(ca_certs=config.PATH_TO_ROOT_CA)

mqtt_client.username_pw_set(username='noor', password='noor1234')
mqtt_client.connect(config.IOT_ENDPOINT, port=8883, keepalive=60)

def publish_data():
    mqtt_client.loop_start()  # Start the loop to process network traffic

    while True:
        temperature = get_temperature()
        humidity = get_humidity()
        
        payload = json.dumps({
            "temperature": temperature,
            "humidity": humidity
        })

        result = mqtt_client.publish(config.SENSOR_DATA_TOPIC, payload, qos=1)
        result.rc  # Check result code (0 means success)

        print(f"Published data: {payload}")

        time.sleep(1) #Every 1 second it is updated

if __name__ == "__main__":
    publish_data()
    mqtt_client.loop_stop()  # Stop the loop when done
