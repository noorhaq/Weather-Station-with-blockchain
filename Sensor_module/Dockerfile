# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the entire SENSOR_MODULE folder into the container
COPY . /usr/src/app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional packages required by the scripts
RUN pip install --no-cache-dir paho-mqtt aiocoap

# Expose the ports used by the MQTT client and CoAP server
EXPOSE 8883 5683

# Run the coap server and mqtt client when the container launches
CMD ["sh", "-c", "python coap_server.py & python mqtt_client.py"]