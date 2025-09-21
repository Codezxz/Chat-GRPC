import os, asyncio, signal, logging
import grpc
from generated import chat_pb2_grpc
from server.service import ChatServicer

async def serve():
    port = os.getenv("PORT", "50051")
    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f"0.0.0.0:{port}")
    await server.start()
    print(f"gRPC server listening on {port}")

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, stop_event.set)
    loop.add_signal_handler(signal.SIGTERM, stop_event.set)
    await stop_event.wait()
    await server.stop(grace=5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
