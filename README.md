# Chat-GRPC

## Features
- Async gRPC server using `grpc.aio`
- WebSocket bridge using FastAPI to connect browser clients to gRPC backend
- Modular code: `server/`, `proto/`, `bridge/`, `client/`
- Dockerfile for containerized deployment

## Run (local)
1. Install deps: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
2. Generate protobuf Python classes:
```bash
python -m grpc_tools.protoc -I./proto --python_out=./generated --grpc_python_out=./generated proto/chat.proto
