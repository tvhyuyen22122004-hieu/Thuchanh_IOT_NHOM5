import asyncio

import json
from datetime import datetime

import aiocoap


URI = "coap://127.0.0.1:5683/iot/lab/sensor01/data"


def show_data(data):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Received sensor data")
    print(f"Device: {data['device_id']}")
    print(f"Temperature: {data['temperature']} C")
    print(f"Humidity: {data['humidity']} %")
    warnings = []
    if data["temperature"] > 35:
        warnings.append("CANH BAO: Nhiet do cao")
    if data["humidity"] < 40:
        warnings.append("CANH BAO: Do am thap")
    if warnings:
        print("\n".join(warnings))
    else:
        print("Trang thai: Binh thuong")
    print("-" * 30)


async def main():
    protocol = await aiocoap.Context.create_client_context()
    print("Monitoring CoAP Client started. Nhan Ctrl+C de dung.")
    try:
        while True:
            try:
                response = await protocol.request(aiocoap.Message(code=aiocoap.GET, uri=URI)).response
                if not response.code.is_successful():
                    print(f"Server phan hoi loi: {response.code}")
                else:
                    show_data(json.loads(response.payload.decode("utf-8")))
            except (json.JSONDecodeError, UnicodeDecodeError) as error:
                print(f"Du lieu JSON khong hop le: {error}")
            except Exception as error:
                print(f"Khong the lay du lieu cam bien: {error}")
            await asyncio.sleep(3)
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring Client stopped")
