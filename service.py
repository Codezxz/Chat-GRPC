import asyncio, time, uuid
from generated import chat_pb2, chat_pb2_grpc

class ChatServicer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self._clients = set()
        self._lock = asyncio.Lock()

    async def Chat(self, request_iterator, context):
        q = asyncio.Queue()
        async with self._lock:
            self._clients.add(q)

        async def writer():
            try:
                while True:
                    msg = await q.get()
                    if msg is None:
                        break
                    yield msg
            finally:
                return

        async def reader():
            try:
                async for incoming in request_iterator:
                    if not incoming.id:
                        incoming.id = str(uuid.uuid4())
                    if not incoming.ts:
                        incoming.ts = int(time.time() * 1000)
                    await self._broadcast(incoming)
            except Exception:
                pass

        reader_task = asyncio.create_task(reader())
        try:
            async for out_msg in writer():
                yield out_msg
        finally:
            reader_task.cancel()
            async with self._lock:
                self._clients.discard(q)

    async def _broadcast(self, message):
        async with self._lock:
            clients = list(self._clients)
        for q in clients:
            try:
                q.put_nowait(message)
            except asyncio.QueueFull:
                try:
                    _ = q.get_nowait()
                except Exception:
                    pass
                try:
                    q.put_nowait(message)
                except Exception:
                    pass
