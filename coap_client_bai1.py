import asyncio


import aiocoap


URI = "coap://127.0.0.1:5683/iot/lab/message"
STUDENT_ID = "B23DCCN313"
STUDENT_NAME = "Tran Van Hieu"


def show_response(response):
    print("Response:")
    print(f"Code: {response.code}")
    print(f"Payload: {response.payload.decode('utf-8', errors='replace')}")


async def main():
    protocol = await aiocoap.Context.create_client_context()
    try:
        print("CoAP Client")
        print("Sending GET request...")
        print(f"URI: {URI}")
        response = await protocol.request(aiocoap.Message(code=aiocoap.GET, uri=URI)).response
        show_response(response)
        payload = f"Xin chao tu CoAP Client - {STUDENT_ID} - {STUDENT_NAME}"
        print("Sending POST request...")
        print(f"Payload: {payload}")
        response = await protocol.request(
            aiocoap.Message(code=aiocoap.POST, uri=URI, payload=payload.encode("utf-8"))
        ).response
        show_response(response)
    except Exception as error:
        print(f"Loi ket noi CoAP: {error}")
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
