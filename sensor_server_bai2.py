import asyncio

import json
import random
from datetime import datetime

import aiocoap.resource as resource
import aiocoap


class SensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.data = self.create_reading()

    @staticmethod
    def create_reading():
        return {
            "device_id": "sensor01",
            "temperature": round(random.uniform(25.0, 38.0), 1),
            "humidity": round(random.uniform(35.0, 75.0), 1),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

    def update(self):
        self.data = self.create_reading()
        print(f"Updated sensor data: {json.dumps(self.data, ensure_ascii=False)}")

    async def render_get(self, request):
        print("GET request received: /iot/lab/sensor01/data")
        payload = json.dumps(self.data, ensure_ascii=False).encode("utf-8")
        return aiocoap.Message(code=aiocoap.CONTENT, payload=payload, content_format=50)


async def update_sensor(resource_instance):
    while True:
        await asyncio.sleep(3)
        resource_instance.update()


async def main():
    sensor = SensorResource()
    root = resource.Site()
    root.add_resource(["iot", "lab", "sensor01", "data"], sensor)
    await aiocoap.Context.create_server_context(root, bind=("0.0.0.0", 5683))
    print("Sensor CoAP Server started on port 5683")
    print("Resource: /iot/lab/sensor01/data")
    print(f"Initial sensor data: {json.dumps(sensor.data, ensure_ascii=False)}")
    await update_sensor(sensor)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSensor CoAP Server stopped")
