### Senosr_module

docker build -t sensor-node .

docker run -it -p 8883:8883 -p 5683:5683 sensor-node

docker network create coap_network

docker run -d --name COAPServer --network coap_network -p 5683:5683 -p 8883:8883 sensor-node

docker run -d --name COAPClient --network coap_network -p 8000:8000 server_module
