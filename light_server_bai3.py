"""CoAP server: giam sat va dieu khien den, ho tro Observe."""
import asyncio
import json
from datetime import datetime

import aiocoap
import aiocoap.resource as resource


class LightResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.state = "OFF"
        self.updated_at = datetime.now().isoformat(timespec="seconds")

    def payload(self):
        return json.dumps({
            "device_id": "light01",
            "state": self.state,
            "updated_at": self.updated_at,
        }, ensure_ascii=False).encode("utf-8")

    async def render_get(self, request):
        print("GET/OBSERVE: /iot/lab/light01/status")
        return aiocoap.Message(code=aiocoap.CONTENT, payload=self.payload(), content_format=50)

    async def render_put(self, request):
        try:
            command = request.payload.decode("utf-8").strip().upper()
        except UnicodeDecodeError:
            return aiocoap.Message(code=aiocoap.BAD_REQUEST, payload="Payload phai la UTF-8".encode())
        if command not in ("ON", "OFF"):
            return aiocoap.Message(code=aiocoap.BAD_REQUEST, payload=b"Chi chap nhan ON hoac OFF")
        if command != self.state:
            self.state = command
            self.updated_at = datetime.now().isoformat(timespec="seconds")
            print(f"Den da chuyen sang {self.state} luc {self.updated_at}")
            self.updated_state()  # Gui thong bao Observe cho cac client dang theo doi
        else:
            print(f"Den da o trang thai {self.state}; khong can cap nhat")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.payload(), content_format=50)


async def main():
    root = resource.Site()
    light = LightResource()
    root.add_resource(["iot", "lab", "light01", "status"], light)
    await aiocoap.Context.create_server_context(root, bind=("0.0.0.0", 5683))
    print("Light CoAP Server dang chay tai cong UDP 5683")
    print("Resource: coap://127.0.0.1:5683/iot/lab/light01/status")
    print("Trang thai ban dau: OFF. Nhan Ctrl+C de dung.")
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nLight CoAP Server da dung")
