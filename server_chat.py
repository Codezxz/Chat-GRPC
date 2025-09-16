import asyncio
from grpc.experimental import aio
import chat_pb2
import chat_pb2_grpc
from loguru import logger

# Keep track of all connected clients' request iterators
connected_clients = set()

class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    async def ChatStream(self, request_iterator, context):
        # Add this client's iterator
        connected_clients.add(request_iterator)
        try:
            async for chat_msg in request_iterator:
                # Broadcast to all other clients
                for client_iter in connected_clients:
                    if client_iter != request_iterator:
                        await context.write(chat_pb2.ChatMessage(
                            username=chat_msg.username,
                            message=chat_msg.message
                        ))
        finally:
            connected_clients.remove(request_iterator)

async def serve():
    server = aio.server()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port('[::]:50052')
    await server.start()
    logger.info("Async gRPC chat server running on 50052")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
