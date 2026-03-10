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
    server_task = asyncio.create_task(server.start_server())
    await asyncio.sleep(0.1)  # Allow server to start

    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    writer.write(b"Hello\n")
    await writer.drain()

    server_task.cancel()