import asyncio, time, uuid, grpc
from generated import chat_pb2, chat_pb2_grpc

async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as ch:
        stub = chat_pb2_grpc.ChatServiceStub(ch)

        async def gen():
            for i in range(1, 6):
                yield chat_pb2.ChatMessage(
                    user='client',
                    text=f'msg {i}',
                    ts=int(time.time()*1000),
                    id=str(uuid.uuid4())
                )
                await asyncio.sleep(1)

        async for msg in stub.Chat(gen()):
            print('recv', msg.user, msg.text)

if __name__ == "__main__":
    asyncio.run(run())
