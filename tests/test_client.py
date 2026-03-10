import pytest
import asyncio
from client import ChatClient
from server import ChatServer

@pytest.mark.asyncio
async def test_client_connection():
    server = ChatServer()
    server_task = asyncio.create_task(server.start_server())
    await asyncio.sleep(0.1)  # Allow server to start

    client = ChatClient()
    connect_task = asyncio.create_task(client.run())
    await asyncio.sleep(0.1)  # Allow client to connect
    assert connect_task.done() is False

    connect_task.cancel()
    server_task.cancel()

@pytest.mark.asyncio
async def test_send_message():
    server = ChatServer()
    server_task = asyncio.create_task(server.start_server())
    await asyncio.sleep(0.1)  # Allow server to start

    client = ChatClient()
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    writer.write(b"Test message\n")
    await writer.drain()
    data = await reader.read(100)
    assert data.decode().strip() == "Test message"

    server_task.cancel()