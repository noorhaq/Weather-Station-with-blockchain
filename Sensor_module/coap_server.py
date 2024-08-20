import asyncio
import aiocoap
from aiocoap import resource
import config
import weather_data

class TemperatureServer(resource.Resource):

    async def render_get(self, request):
        temperature = weather_data.get_temperature()
        payload = f"temperature={temperature}"
        print (payload)
        return aiocoap.Message(code=aiocoap.Code.CONTENT, payload=payload.encode())

class HumidityServer(resource.Resource):
    async def render_get(self, request):
        humidity = weather_data.get_humidity()
        payload = f"humidity={humidity}"
        return aiocoap.Message(code=aiocoap.Code.CONTENT, payload=payload.encode())

async def main():
    root = resource.Site()
    root.add_resource(['temperature'], TemperatureServer())
    root.add_resource(['humidity'], HumidityServer())

    await aiocoap.Context.create_server_context(root, bind=(config.COAP_SERVER_IP, 5683))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()