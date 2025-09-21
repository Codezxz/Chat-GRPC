import os
import grpc
from concurrent import futures
import chat_pb2_grpc

def serve():
    port = os.getenv("PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    print(f"gRPC server listening on port {port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
