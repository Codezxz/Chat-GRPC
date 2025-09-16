from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import asyncio
from grpc.experimental import aio
from google.protobuf.wrappers_pb2 import StringValue
import chat_pb2
import chat_pb2_grpc

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Keep track of all WebSocket clients
websocket_clients = set()

@app.websocket("/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    websocket_clients.add(ws)
    send_queue = asyncio.Queue()

    # Async generator sending WebSocket → gRPC messages
    async def ws_to_grpc():
        while True:
            msg = await send_queue.get()
            yield msg

    # Task: Listen to gRPC stream and broadcast to WebSocket clients
    async def grpc_to_ws():
        async with aio.insecure_channel("localhost:50052") as channel:
            stub = chat_pb2_grpc.ChatServiceStub(channel)
            grpc_iterator = ws_to_grpc().__aiter__()  # proper async iterator
            async for grpc_msg in stub.ChatStream(grpc_iterator):
                to_remove = []
                for client in websocket_clients:
                    try:
                        await client.send_json({
                            "username": grpc_msg.username.value,
                            "message": grpc_msg.message.value
                        })
                    except:
                        to_remove.append(client)
                for client in to_remove:
                    websocket_clients.remove(client)

    # Start the background task only once per WebSocket connection
    asyncio.create_task(grpc_to_ws())

    # Read messages from WebSocket → push to gRPC
    try:
        while True:
            data = await ws.receive_json()
            chat_msg = chat_pb2.ChatMessage(
                username=StringValue(value=data.get("username")),
                message=StringValue(value=data.get("message"))
            )
            await send_queue.put(chat_msg)
    except:
        websocket_clients.remove(ws)
