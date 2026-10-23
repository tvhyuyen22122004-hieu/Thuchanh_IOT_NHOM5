"""Monitoring client dang ky CoAP Observe de nhan thay doi trang thai den."""
import asyncio
import json
from datetime import datetime

import aiocoap

URI = "coap://127.0.0.1:5683/iot/lab/light01/status"


def show_response(response):
    try:
        data = json.loads(response.payload.decode("utf-8"))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Den {data['device_id']}: {data['state']} | cap nhat: {data['updated_at']}")
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Khong doc duoc du lieu: {error}; payload={response.payload!r}")


async def main():
    protocol = await aiocoap.Context.create_client_context()
    request = protocol.request(aiocoap.Message(code=aiocoap.GET, uri=URI, observe=0))
    try:
        response = await request.response
        if not response.code.is_successful():
            print(f"Server phan hoi loi: {response.code}")
            return
        print("Da dang ky CoAP Observe. Thay doi trang thai bang light_controller_bai3.py.")
        print("Client se nhan thong bao khi trang thai den thay doi; nhan Ctrl+C de dung.")
        show_response(response)
        if request.observation is None:
            print("Server khong chap nhan Observe; hay kiem tra light_server_bai3.py.")
            return
        request.observation.register_callback(show_response)
        await request.observation.wait()
    except asyncio.CancelledError:
        pass
    except Exception as error:
        print(f"Loi khi theo doi den: {error}")
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring Client da dung")
