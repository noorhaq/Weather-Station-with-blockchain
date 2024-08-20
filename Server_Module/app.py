import logging
from quart import Quart, jsonify, render_template
from coap_client import CoAPClient
import mqtt_broker
import asyncio
import time
import threading

app = Quart(__name__)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)
# Create a CoAP client instance
client = CoAPClient()

# Initialize the CoAP client connection
async def init_coap_client():
    while True:
        try:
            await client.connect()
            return True
        except Exception as e:
            logger.error(f"Error connecting to CoAP client: {e}")
            await asyncio.sleep(30)  # retry every 30 seconds
            return False

# Define API endpoints
coap_connected = False

@app.before_serving
async def init_coap():
    global coap_connected
    coap_connected = await init_coap_client()

@app.before_serving
async def startup_event():
    logger.info("Starting MQTT client")
    asyncio.create_task(mqtt_broker.start_mqtt_client())


@app.route('/coap/temperature', methods=['GET'])
async def coap_temperature():
    """Get temperature from CoAP server"""
    if coap_connected:
        try:
            temperature = await client.fetch_temperature()
            return jsonify({'temperature': temperature})
        except Exception as e:
            logger.error(f"Error fetching temperature from CoAP: {e}")
            return jsonify({'error': f"Error fetching temperature from CoAP: {e}"}), 500
    else:
        return jsonify({'error': 'CoAP client not connected'}), 500

@app.route('/coap/humidity', methods=['GET'])
async def coap_humidity():
    """Get humidity from CoAP server"""
    if coap_connected:
        try:
            humidity = await client.fetch_humidity()
            return jsonify({'humidity': humidity})
        except Exception as e:
            logger.error(f"Error fetching humidity from CoAP: {e}")
            return jsonify({'error': f"Error fetching humidity from CoAP: {e}"}), 500
    else:
        return jsonify({'error': 'CoAP client not connected'}), 500

@app.route('/mqtt/temperature', methods=['GET'])
async def mqtt_temperature():
    """Get temperature from MQTT broker"""
    try:
        return jsonify({'temperature': mqtt_broker.fetch_temperature()})
    except Exception as e:
        logger.error(f"Error fetching temperature from MQTT: {e}")
        return jsonify({'error': f"Error fetching temperature from MQTT: {e}"}), 500

@app.route('/mqtt/humidity', methods=['GET'])
async def mqtt_humidity():
    """Get humidity from MQTT broker"""
    try:
        return jsonify({'humidity': mqtt_broker.fetch_humidity()})
    except Exception as e:
        logger.error(f"Error fetching humidity from MQTT: {e}")
        return jsonify({'error': f"Error fetching humidity from MQTT: {e}"}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
async def catch_all(path):
    return await render_template("index.html")

# if __name__ == '__main__':
#     # Start the MQTT client thread
#     stop_event = mqtt_broker.start_mqtt_client_thread()

#     # Run the Quart app
#     try:
#         app.run(host='0.0.0.0', port=8000)
#     except Exception as e:
#         logger.error(f"Error running Quart app: {e}")

#     # Stop the MQTT client thread
#     try:
#         stop_event.set()
#         mqtt_broker.mqtt_thread.join()
#     except Exception as e:
#         logger.error(f"Error stopping MQTT client thread: {e}")