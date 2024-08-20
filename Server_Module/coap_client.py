# coap_client.py
import asyncio
import aiocoap
import json
import logging
from typing import Optional

from config import COAP_SERVER_IP

class CoAPClient:
    def __init__(self):
        self.protocol = None
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        try:
            self.protocol = await aiocoap.Context.create_client_context()
        except Exception as e:
            self.logger.error(f'Failed to connect to CoAP server: {e}')
            raise

    async def fetch_temperature(self) -> Optional[float]:
        try:
            request = aiocoap.Message(code=aiocoap.Code.GET, uri=(COAP_SERVER_IP + '/temperature'))
            response = await self.protocol.request(request).response
            payload = response.payload.decode()
            temperature = float(payload.split('=')[1])
            return temperature
        except Exception as e:
            self.logger.error(f'Failed to fetch temperature: {e}')
            return None

    async def fetch_humidity(self) -> Optional[float]:
        try:
            request = aiocoap.Message(code=aiocoap.Code.GET, uri=(COAP_SERVER_IP + '/humidity'))
            response = await self.protocol.request(request).response
            payload = response.payload.decode()
            humidity = float(payload.split('=')[1])
            return humidity
        except Exception as e:
            self.logger.error(f'Failed to fetch humidity: {e}')
            return None

    async def get_data(self, type: str) -> Optional[float]:
        if type == 'temperature':
            return await self.fetch_temperature()
        elif type == 'humidity':
            return await self.fetch_humidity()
        else:
            self.logger.error(f'Invalid data type: {type}')
            return None

    async def close(self):
        if self.protocol:
            await self.protocol.shutdown()

async def main():
    client = CoAPClient()
    await client.connect()
    try:
        # Create a dictionary to store the results
        # results = {}

        # Get temperature and humidity data
        # results['temperature'] = await client.fetch_temperature()
        # results['humidity'] = await client.fetch_humidity()
        print(await client.fetch_temperature())
        # Print the results
        # print(json.dumps(results))
    finally:
        await client.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())