"""Controller dieu khien den qua CoAP PUT."""
import asyncio
import aiocoap

URI = "coap://127.0.0.1:5683/iot/lab/light01/status"


async def main():
    protocol = await aiocoap.Context.create_client_context()
    print("Dieu khien den: nhap ON, OFF, STATUS hoac EXIT")
    try:
        while True:
            try:
                command = (await asyncio.to_thread(input, "Lenh> ")).strip().upper()
            except EOFError:
                break
            if command == "EXIT":
                break
            if command == "STATUS":
                message = aiocoap.Message(code=aiocoap.GET, uri=URI)
            elif command in ("ON", "OFF"):
                message = aiocoap.Message(code=aiocoap.PUT, uri=URI, payload=command.encode("utf-8"))
            else:
                print("Lenh khong hop le. Hay nhap ON, OFF, STATUS hoac EXIT.")
                continue
            try:
                response = await protocol.request(message).response
                print(f"Phan hoi Server [{response.code}]: {response.payload.decode('utf-8', errors='replace')}")
            except Exception as error:
                print(f"Khong ket noi duoc Server: {error}")
    finally:
        await protocol.shutdown()
    print("Controller da dung")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nController da dung")
