## Instructions

- **Sensor Module** - To run the sensor module and server module on the same system use the docker compose up file with the environment variable COAP_URL set to the correct address. As right now it points to the other cointainer address.
  Use this command
  `docker-compose up` - To run the sensor module seperately make small edits in the `cofig.py` file
  To point to the correct `COAP_SERVER_IP` then use the following steps to build the docker file

`docker build -t sensor_module .`
`docker run -p 8883:8883 -p 5683::5683 sensor_module`
The above commands will build and run the docker cointainer for the sensor module with the ports 8883 and 5683 exposed for MQTT and COAP communications.

- **Server Module** - To run the sensor module and server module on the same system use the docker compose up file with the environment variable COAP_URL set to the correct address. As right now it points to the other cointainer address.
  Use this command
  `docker-compose up` - To run the sensor module seperately make small edits in the `cofig.py` file
  To point to the correct `COAP_SERVER_IP` then use the following steps to build the docker file

`docker build -t server_module .`
`docker run -p 8883:8883 -p 5683::5683 -p 8000:8000 sensor_module`
The above commands will build and run the docker cointainer for the sensor module with the ports 8883 and 5683 exposed for MQTT and COAP communications. And the 8000 port is to display a HTML page with 2 buttons for the humidty and temperature for both the COAP and MQTT. And it will update everytime the button is clicked. If running locally you can access the webpage on `127.0.0.1::8000`

- **BlockChain** - In this we are using the solana blockchain for that first we have to first run the local solana cluster which is optional 1. `solana-test-validator` 2. cd Blockchain
  cd weather_data
  anchor build
  anchor deploy
  This will output the program ID which we will need later to add in the config.rs file. 3. Now in another terminal go to

          cd weather_recorder
          cargo run

  We can switch to mainnet by changing the RPC URL but we have to make sure we have enough SOL for the transaction.
