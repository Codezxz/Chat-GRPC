import os

async def serve():
    port = os.getenv("PORT", "50051")  # Render sets PORT
    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    listen_addr = f"0.0.0.0:{port}"
    server.add_insecure_port(listen_addr)
    await server.start()
    print(f"gRPC server started on {listen_addr}")
    await server.wait_for_termination()
