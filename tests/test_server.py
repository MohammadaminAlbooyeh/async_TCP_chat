import pytest
import asyncio
from server import ChatServer

@pytest.mark.asyncio
async def test_server_startup():
    server = ChatServer()
    server_task = asyncio.create_task(server.start_server())
    await asyncio.sleep(0.1)  # Allow server to start
    assert server_task.done() is False
    server_task.cancel()

@pytest.mark.asyncio
async def test_handle_client():
    server = ChatServer()
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    server_task = asyncio.create_task(server.start_server())
    await asyncio.sleep(0.1)
    writer.write(b"Hello\n")
    await writer.drain()
    await asyncio.sleep(0.1)
    assert len(server.clients) > 0
    server_task.cancel()