import asyncio

from datetime import datetime

import aiocoap.resource as resource
import aiocoap


class MessageResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.latest_message = None

    async def render_get(self, request):
        print("GET request received: /iot/lab/message")
        payload = "Xin chao tu CoAP Server"
        if self.latest_message:
            payload = f"{payload}\nThong diep gan nhat: {self.latest_message}"
        return aiocoap.Message(code=aiocoap.CONTENT, payload=payload.encode("utf-8"))

    async def render_post(self, request):
        try:
            message = request.payload.decode("utf-8").strip()
        except UnicodeDecodeError:
            return aiocoap.Message(code=aiocoap.BAD_REQUEST, payload=b"Payload phai la UTF-8")
        if not message:
            return aiocoap.Message(code=aiocoap.BAD_REQUEST, payload=b"Thong diep khong duoc de trong")
        self.latest_message = message
        print("POST request received:")
        print(f"Payload: {message}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b"Server da nhan thong diep")


async def main():
    root = resource.Site()
    root.add_resource(["iot", "lab", "message"], MessageResource())
    await aiocoap.Context.create_server_context(root, bind=("0.0.0.0", 5683))
    print("CoAP Server started on port 5683")
    print("Resource: /iot/lab/message")
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCoAP Server stopped")
